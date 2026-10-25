
from datetime import datetime


class CustomerDataset:
    def __init__(self, customers: list, source: str):
        self.customers_data = customers
        self.source = source
        self.last_update = datetime.now()

    def __contains__(self, customer_name: str) -> bool:
        # return any(c.get("name") == customer_name for c in self.customers_data)
        return [c for c in self.customers_data if c.get("name") == customer_name]

    def __repr__(self) -> str:
        return f"CustomerDataset({len(self.customers_data)} customers from '{self.source}')"

    def __len__(self) -> int:
        return len(self.customers_data)

    def filter_customers(self, min_age: int) -> list:
        return [c for c in self.customers_data if c.get("age", 0) >= min_age]

    def add_customer(self, name: str, age: int):
        self.customers_data.append({"name": name, "age": age})
        self.last_update = datetime.now()

    def update_data(self, new_data: list):
        self.customers_data = new_data
        self.last_update = datetime.now()

    def display_info(self):
        formatted_date = self.last_update.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Источник: {self.source}")
        print(f"Последнее обновление: {formatted_date}")
        print(f"Количество покупателей: {len(self.customers_data)}")


class PremiumCustomerDataset(CustomerDataset):
    def __init__(self, customers: list, source: str, membership_level: str):
        super().__init__(customers, source)
        self.membership_level = membership_level

    def filter_by_membership(self, level: str) -> list:
        return [c for c in self.customers_data if c.get("membership") == level]

    def display_info(self):
        super().display_info()
        print(f"Уровень членства: {self.membership_level}")
