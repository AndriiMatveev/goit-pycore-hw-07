import calendar
from collections import UserDict
from datetime import date, timedelta

from record import Record


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name not in self.data:
            raise KeyError(f"Contact {name} not found.")
        del self.data[name]

    def get_upcoming_birthdays(self) -> list:
        today = date.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value
            is_leap_birthday = birthday.month == 2 and birthday.day == 29

            if is_leap_birthday and not calendar.isleap(today.year):
                birthday_this_year = date(today.year, 3, 1)
            else:
                birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                if is_leap_birthday and not calendar.isleap(today.year + 1):
                    birthday_this_year = date(today.year + 1, 3, 1)
                else:
                    birthday_this_year = birthday.replace(year=today.year + 1)

            days_until_birthday = (birthday_this_year - today).days

            if 0 <= days_until_birthday <= 7:
                congratulation_date = birthday_this_year
                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                })

        return upcoming_birthdays
