from address_book import AddressBook
from record import Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return e.args[0] if e.args else "Contact not found."
        except IndexError:
            return "Not enough arguments."

    return inner


def parse_input(user_input: str) -> tuple:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def get_record(book: AddressBook, name: str) -> Record:
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")
    return record


@input_error
def add_contact(args: list, book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Usage: add [name] [phone]")
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        message = "Contact added."
    record.add_phone(phone)
    book.add_record(record)
    return message


@input_error
def change_contact(args: list, book: AddressBook) -> str:
    if len(args) < 3:
        raise ValueError("Usage: change [name] [old phone] [new phone]")
    name, old_phone, new_phone, *_ = args
    record = get_record(book, name)
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args: list, book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("Usage: phone [name]")
    record = get_record(book, args[0])
    if not record.phones:
        return f"{record.name} has no phones."
    return f"{record.name}: {'; '.join(p.value for p in record.phones)}"


@input_error
def show_all(book: AddressBook) -> str:
    if not book.data:
        return "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args: list, book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Usage: add-birthday [name] [DD.MM.YYYY]")
    name, birthday, *_ = args
    record = get_record(book, name)
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args: list, book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("Usage: show-birthday [name]")
    record = get_record(book, args[0])
    if record.birthday is None:
        return f"{record.name} has no birthday set."
    return f"{record.name}: {record.birthday}"


@input_error
def birthdays(args: list, book: AddressBook) -> str:
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."
    return "\n".join(f"{item['name']}: {item['congratulation_date']}" for item in upcoming)


def main() -> None:
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        try:
            user_input = input("Enter a command: ")
        except (KeyboardInterrupt, EOFError):
            print("\nGood bye!")
            break

        if not user_input.strip():
            continue

        command, *args = parse_input(user_input)

        match command:
            case "close" | "exit":
                print("Good bye!")
                break
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, book))
            case "change":
                print(change_contact(args, book))
            case "phone":
                print(show_phone(args, book))
            case "all":
                print(show_all(book))
            case "add-birthday":
                print(add_birthday(args, book))
            case "show-birthday":
                print(show_birthday(args, book))
            case "birthdays":
                print(birthdays(args, book))
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()