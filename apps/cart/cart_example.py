from decimal import Decimal


class Cart():
    def __init__(self, cart):
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()

        cart = self.cart.copy()

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"]*item["quantity"]
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        # total_price = 0
        # for item in self.cart.values():
        #     total_price += Decimal(item["price"]) * item["quantity"]
        # return total_price
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values())


data = {
    "12":{"quantity":1, "price":"1200"},
    "13":{"quantity":4, "price":"1400"},
    "14":{"quantity":3, "price":"4200"},
}

cart = Cart(data)

for i in cart:
    print(i)
print(len(cart))
print(cart.get_total_price())