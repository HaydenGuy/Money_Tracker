from typing import Union

class Item():
    def __init__(self, name: str, price: Union[int, float]):
        self.name = name
        self.price = price

test_item = Item("Food", 50.0)
test_item2 = Item("Phone", 27)