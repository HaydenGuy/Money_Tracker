from typing import Union

class Item:
    def __init__(self, name: str, price: Union[int, float], category: str):
        self.name = name
        self.price = price
        self.valid_category(category)
        self.category = category

    # Check that the category is in the list of valid options and return ValueError if not
    def valid_category(self, category: str):
        valid_options = ("RENT", "GROCERIES", "BILLS", "SUBSCRIPTIONS", "HOUSEHOLD", "RESTAURANTS", "ENTERTAINMENT", "OTHER")
        if category not in valid_options:
            raise ValueError(f"Invalid category: {category}\nValid categories: {valid_options}")


test_item = Item("Food", 50.0, "GROCERIES")
test_item2 = Item("Phone", 27, "BILLS")
print(test_item.category)
print(test_item2)