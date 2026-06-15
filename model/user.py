class User:

    def __init__(self, id, username, email, password, role):
        self.id = id
        self.username = username
        self.email = email
        self.password = password  # hash bcrypt
        self.role = role          # "user" | "admin"

    def __str__(self):
        return f"{self.username} ({self.email}) - {self.role}"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def to_dict(self):
        return {
            "id":       self.id,
            "username": self.username,
            "email":    self.email,
            "role":     self.role,
            # La password NON viene mai restituita nelle risposte HTTP
        }
