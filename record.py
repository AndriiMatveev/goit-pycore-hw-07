from birthday import Birthday
from name import Name
from phone import Phone


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str) -> None:
        if self.find_phone(phone) is not None:
            raise ValueError(f"Phone {phone} already exists for {self.name}.")
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        found = self.find_phone(phone)
        if found is None:
            raise ValueError(f"Phone {phone} not found.")
        self.phones.remove(found)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        found = self.find_phone(old_phone)
        if found is None:
            raise ValueError(f"Phone {old_phone} not found.")
        index = self.phones.index(found)
        self.phones[index] = Phone(new_phone)

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones) or "-"
        birthday = str(self.birthday) if self.birthday else "-"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"
