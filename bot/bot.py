from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton as ibutton
from text import StaticTexts
from api import sApi
from markup import StaticMarkups
from dotenv import load_dotenv
from colorama import Fore

import colorama
import requests
import telebot
import os
import json
load_dotenv()
colorama.init(autoreset=True)


TOKEN: str = os.getenv('TOKEN')
API: str = os.getenv('API')
bot = telebot.TeleBot(TOKEN) 

Api = sApi()


def callback(prefix, data={}):
    res = {
        "prefix":prefix,
        "data": data
    }
    return str(res).replace("'", '"')

class sDynamicText(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(sDynamicText, cls).__new__(cls)
        return cls.instance
    
    def convert_product_to_str(self, _type, _product):
        match _type:
            case "v2ray":
                return (
                    f"{_product['expire_time']} روزه - {_product['volume']} گیگ "
                )
        return ("خالی")
        
DynamicText = sDynamicText()  

class sDynamicMarkup(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(sDynamicMarkup, cls).__new__(cls)
        return cls.instance
    

    def markup_operator(self):
        markup = InlineKeyboardMarkup(row_width=1)
        for v2ray_operator in Api.v2ray_operator_all['data']:
            markup.add(
                ibutton(
                    text=str(v2ray_operator['title']),
                    callback_data=callback("v2ray_operator", data={'op_id': v2ray_operator['id']})
                )
            )
        return markup
    
    def markup_select_product(self, operator_id):
        markup = InlineKeyboardMarkup(row_width=1)
        for _v2ray in Api.v2ray_all['data']:
            
            if int(operator_id) in [i['id'] for i in (_v2ray['operator'])]: # filter products by operator id
                if _v2ray['expire_time'] == 0:
                    markup.add(
                        ibutton(
                            text=f"بدون محدودیت زمانی - {_v2ray['volume']} گیگ {int(_v2ray['price']):,} تومان",
                            callback_data=callback("v2ray_product", data={'op_id': operator_id, 'pr_id': _v2ray['id']})
                        )
                    )
                    
                elif _v2ray['expire_time'] == 30:
                    markup.add(
                        ibutton(
                            text=f"یک ماهه - {_v2ray['volume']} گیگ {int(_v2ray['price']):,} تومان" ,
                            callback_data=callback("v2ray_product", data={'op_id': operator_id, 'pr_id': _v2ray['id']})
                        )
                    )
                    
                else :
                    markup.add(
                        ibutton(
                            text=f"{_v2ray['expire_time']} روزه - {_v2ray['volume']} گیگ {int(_v2ray['price']):,} تومان",
                            callback_data=callback("v2ray_product", data={'op_id': operator_id, 'pr_id': _v2ray['id']})
                        )
                    ) 
                                
        return markup

DynamicMarkup = sDynamicMarkup()

class MainMessage(object):
    
    chat_id = None
    message_id = None
    message = None
    
    def __init__(self, message):
        self.chat_id = message.chat.id
        self.message_id = message.id
        self.message = message
        
        bot.send_message(self.chat_id, self.main_text(), reply_markup=self._markup())
    
    def _markup(self):
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(*[
            ibutton(
                text="کانفیگ های من 📱",
                callback_data=callback("my_configs")
            ),
            ibutton(
                text="خرید کانفیگ جدید 🛒",
                callback_data=callback("buy_new_config")
            )
        ],)
        
        markup.add(
            ibutton(
                text="دریافت اکانت تست 🎁",
                callback_data=callback("test_config")
        ))
        
        markup.add(
            ibutton(
                text="شارژ کیف پول 💳",
                callback_data=callback("add_credit")
        ))
        
        markup.add(*[
            ibutton(
                text="زیرمجموعه گیری 🏆",
                callback_data=callback("subcategory")
            ),
            ibutton(
                text="حساب کاربری 👩‍💼",
                callback_data=callback("account")
            ),
        ])
        markup.add(*[
            ibutton(
                text="آموزش اتصال 🧩",
                callback_data=callback("how_to_connect")
            ),
            ibutton(
                text="ارتباط با ادمین 👨‍💻",
                callback_data=callback("admin_ticket")
            )
        ])
        
        markup.add(
            ibutton(
                text="استعلام کانفیگ 🔋",
                callback_data=callback("inquiry")
            )
        )
        return markup
    
    def main_text(self):
        return (StaticTexts.main_text)
    
class PaymentMesssage(object):
    product_type = None
    product_id = None
    price = None
    message = None
    
    def __init__(self, chat_id, product_type, product_id, level, message_id=None, order_id=None):
        """_summary_
        
        Args:
            chat_id (_type_): _description_
            product_type (_type_): _description_
            product_id (_type_): _description_
            level (_type_): ["ordering", card_to_card_ordering, credit_ordering]
        """
        self.product_type = product_type
        self.product_id = product_id
        # self.order_id = order_id
        self.order_id = "1"
        
        if level == "ordering":
            # order = Api.create_order()error
            
            bot.send_message(
                chat_id=chat_id,
                text=self._text_ordering_main(),
                reply_markup=self.add_cancel_to_markup(self._markup_ordering())
            )
            
        elif level == "card_to_card_ordering":
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=self._text_ordering_card_to_card(),
            )
            
            bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=self.add_cancel_to_markup(InlineKeyboardMarkup(row_width=1)),
            )
            
        elif level == "credit_ordering":
            pass
        
    def _text_ordering_main(self):
        return (f"{self._text_order_title()}عزیزم چجوری میخوای پرداخت کنی ؟؟")
    
    def _text_ordering_card_to_card(self):
        return (f"{self._text_order_title()}عزیزم مبلغ بالا رو به شمار حساب زیر کارت به کارت کن بعدش عکس فیش تراکنش رو برام بفرست.")
        
    def _text_order_title(self):
        
        product = Api.get_products_by_type_and_id(self.product_type, self.product_id)
        print(product)
        self.price = product['price']
        title: str = DynamicText.convert_product_to_str(self.product_type, product)
        
        return (f"〽️ نام پلن: {title}\n\
            ➖➖➖➖➖➖➖\n\
            💎 قیمت پنل : {int(self.price):,} تومان \n\
            ➖➖➖➖➖➖➖\n"
        )
        
    def _markup_ordering(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            ibutton(
                text="کارت به کارت 💳",
                callback_data=callback("pay_card_to_card", data={"order_id": self.order_id})
            ),
            ibutton(
                text="پراخت با کیف پول 💰",
                callback_data=callback("pay_creadit", data={"order_id": self.order_id})
            ),
        )
        return markup
    
    def add_cancel_to_markup(self, markup):
        markup.add(    
            ibutton(
                    text="منصرف شدم 😪",
                    callback_data=callback("pay_cancel_ordering", data={"order_id": self.order_id}),
                )
        )
        return markup
    
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print((call.data))
    data: dict = json.loads(call.data)
    prefix: str = data['prefix']
    chat_id: int = call.message.chat.id
    message_id: int = call.message.id
            
    match prefix:
#       
        case "buy_new_config":
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=StaticTexts.operator,
            )
            
            bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=DynamicMarkup.markup_operator(),
            )
#
        case "v2ray_operator":
            """_summary_
            - from v2ray_operator to select v2ray product
            - pass operator id to 
            """
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=StaticTexts.select_product,
            )
            
            bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=DynamicMarkup.markup_select_product(data['data']['op_id']),
            )
#           
        case "v2ray_product":
            bot.delete_message(call.message.chat.id, call.message.id)
            PaymentMesssage(
                chat_id=call.message.chat.id,
                product_type="v2ray",
                product_id=data['data']['pr_id'],
                level="ordering",
            )
        
        case "pay_card_to_card":
            PaymentMesssage(
                chat_id=call.message.chat.id,
                product_type=None,
                product_id=None,
                level="card_to_card_ordering", 
            )
        
        case "pay_creadit":
            pass
        
    bot.answer_callback_query(call.id)




@bot.message_handler(commands='start')
def start_command_handler(message: telebot.types.Message):
    MainMessage(message=message)
    
    
     
  
        
        
     


if __name__ == '__main__':
    print("run")
    bot.infinity_polling()
