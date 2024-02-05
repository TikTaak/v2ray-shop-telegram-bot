import uuid 



def create_new_ref_number():
    return str(uuid.uuid4().hex[:6].upper())
    











# def generate():
#     L = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0' ,'1' ,'2' ,'3' ,'4' ,'5' ,'6' ,'7' ,'8' ,'9' ]
#     F = []
#     while not (len(F)==5):
#         F.append(L[random.randint(0, 35)])
#     return str(''.join(F))
    
    
    
# def create_new_ref_number():
#     users = TelegramUser.objects.all()
#     print(users.promo_code)
#     while True:
#         code = generate()
#         if not (generate() in users.promo_code):
#             break
#     return str(code)
    