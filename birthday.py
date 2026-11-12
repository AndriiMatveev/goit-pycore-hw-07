from datetime import date, datetime

from field import Field


class Birthday(Field):
    def __init__(self, value: str):
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        if birthday > date.today():
            raise ValueError("Birthday cannot be in the future.")
        super().__init__(birthday)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
