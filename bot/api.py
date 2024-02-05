from dotenv import load_dotenv

import json
import requests
import os
load_dotenv()

API: str = os.getenv('API')

class sApi(object):
    v2ray_all = None
    v2ray_operator_all = None
    
    def __init__(self):
        self.v2ray_all = json.loads(
            requests.get(
                f"{API}api/v2ray/").text
            )
        
        self.v2ray_operator_all = json.loads(
            requests.get(
                f"{API}api/v2ray/operator/").text
            )
    
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(sApi, cls).__new__(cls)
        return cls.instance
    
    
    def get_products_by_type_and_id(self, _type:str, _id):
        """_summary_
        
        find product by id and type:
        
        Args:
            _type (str): product type
            _id (_type_): product id

        Returns:
            _type_: json 
        """
        match _type:
            case "v2ray":
                # 
                for _product in self.v2ray_all['data']:
                    if _product['id'] == _id:
                        product = _product
                        break
                
                return product
            
            
            
    def create_order(self, ):
        pass
