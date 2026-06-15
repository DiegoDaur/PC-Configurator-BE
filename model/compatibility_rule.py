class CompatibilityRule:

    def __init__(self, id, component_a_id, component_b_id, is_compatible, reason):
        self.id = id
        self.component_a_id = component_a_id
        self.component_b_id = component_b_id
        self.is_compatible = is_compatible
        self.reason = reason

    def __str__(self):
        compat = "OK" if self.is_compatible else "NO"
        return f"CompatibilityRule(a={self.component_a_id}, b={self.component_b_id}, {compat})"

    def to_dict(self):
        return {
            "id":             self.id,
            "component_a_id": self.component_a_id,
            "component_b_id": self.component_b_id,
            "is_compatible":  self.is_compatible,
            "reason":         self.reason,
        }
