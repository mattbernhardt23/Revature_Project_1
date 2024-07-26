import services.user_service as user_service
 
class User:
    def __init__(self):
        self.username = ""
        self.account_balance = 0
        self.admin = False
        self.library = [] 

    def register(self):
        user = user_service.register()
        if user:
            self.username = user["username"]
            self.account_balance = user["account_balance"]
            self.admin = user["admin"]
        return user

    def sign_in(self):
        user = user_service.sign_in()
        if user:
            self.username = user["username"]
            self.account_balance = user["account_balance"]
            self.admin = user["admin"]
        return user
    
    def add_money(self):
        amount = user_service.add_money(self.username)
        if amount:
            self.account_balance += amount
        return amount
    
    def get_library(self):
        self.library = user_service.get_library(self.username)
        return self.library
    
    def print_library(self):
        user_service.print_library(self.library)

    def get_account_balance(self):
        self.account_balance = user_service.get_account_balance(self.username)
    
