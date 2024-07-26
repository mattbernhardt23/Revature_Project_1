import services.inventory_service as inventory_service

class Inventory:
    def __init__(self):
        self.books = []

    def __iter__(self):
        return iter(self.books)
    
    def get_inventory(self):
        books = inventory_service.get_inventory()
        if books:
            self.books = books
        return books
    
    def buy_book(self, username):
        return inventory_service.buy_book(username)
    
    def read_description(self, product_id):
        return inventory_service.read_description(product_id)
    
    def add_book(self):
        return inventory_service.add_book() 
    
    def remove_book(self):
        return inventory_service.remove_book()
    
    def add_to_inventory(self):
        return inventory_service.add_to_inventory()
    
    def print_inventory(self):
        return inventory_service.print_inventory(self.books)
    
    def get_stats(self):
        return inventory_service.get_stats()