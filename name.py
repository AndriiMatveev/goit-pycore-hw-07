from field import Field


class Name(Field):
    def __init__(self, value: str):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value.strip())
