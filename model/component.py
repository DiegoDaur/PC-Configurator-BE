VALID_CATEGORIES = {"CPU", "GPU", "RAM", "Motherboard", "PSU", "Storage", "Case", "Cooler"}


class Component:

    def __init__(self, id, name, brand, category, price, wattage, stock, in_stock, image_url, description, specs):
        self.id = id
        self.name = name
        self.brand = brand
        self.category = category
        self.price = price
        self.wattage = wattage
        self.stock = stock
        self.in_stock = in_stock
        self.image_url = image_url
        self.description = description
        self.specs = specs  # dizionario chiave:valore

    def __str__(self):
        return f"[{self.category}] {self.brand} {self.name} - €{self.price}"

    def __eq__(self, other):
        if not isinstance(other, Component):
            return False
        return self.id == other.id

    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "brand":       self.brand,
            "category":    self.category,
            "price":       self.price,
            "wattage":     self.wattage,
            "stock":       self.stock,
            "in_stock":    self.in_stock,
            "image_url":   self.image_url,
            "description": self.description,
            "specs":       self.specs,
        }
