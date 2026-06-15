class Build:

    def __init__(self, id, user_id, name, notes, created_at, components=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.notes = notes
        self.created_at = created_at
        self.components = components or []  # lista di Component

    def __str__(self):
        return f"{self.name} - {len(self.components)} componenti - €{self.total_price():.2f}"

    def total_price(self):
        return sum(c.price for c in self.components)

    def total_wattage(self):
        return sum(c.wattage for c in self.components)

    def to_dict(self):
        return {
            "id":            self.id,
            "user_id":       self.user_id,
            "name":          self.name,
            "notes":         self.notes,
            "created_at":    str(self.created_at) if self.created_at else None,
            "components":    [{"component": c.to_dict()} for c in self.components],
            "total_price":   self.total_price(),
            "total_wattage": self.total_wattage(),
        }
