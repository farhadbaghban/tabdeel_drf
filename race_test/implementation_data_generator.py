class ImplementationDataGenerator:
    def __init__(self, phone_numbers_count, credit_raises_count, sell_amounts_count):
        self.phone_numbers_count = phone_numbers_count
        self.credit_raises_count = credit_raises_count
        self.sell_amounts_count = sell_amounts_count
        self.phone_numbers = []
        self.credit_raises = []
        self.sell_amounts = []

    def create_phone_numbers(self, iteration):
        for i in range(iteration):
            phone_number = str(22222111110 + i)
            self.phone_numbers.append({"phone_number": phone_number})

    def create_raise_credit_amounts(self, iteration):
        for i in range(iteration):
            amount = 200 + i
            self.credit_raises.append({"amount": amount})

    def create_sell_credit_amounts(self, iteration):
        for i in range(iteration):
            amount = 100 + i
            self.sell_amounts.append({"amount": amount})

    def generate(self):
        self.create_phone_numbers(self.phone_numbers_count)
        self.create_raise_credit_amounts(self.credit_raises_count)
        self.create_sell_credit_amounts(self.sell_amounts_count)
