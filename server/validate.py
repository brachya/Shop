# שם פרטי, שם משפחה, מספר זהות, טלפון, סכום החוב, ותאריך רישום החוב .


class Validate:
    """validate by getting list of customer values and call instance.checked() to
    run all tests and if error filled so there is a wrong value."""

    def __init__(self, customer: list[str]) -> None:
        self.first_name: str = customer[0]
        self.last_name: str = customer[1]
        self.id: str = customer[2]
        self.phone: str = customer[3]
        self.date: str = customer[4]
        self.dept: str = customer[5]
        self.error: str = ""  # for False case

    def first_name_validate(self) -> None:
        """if name has numbers or signs so add to error the explanation of the mistake."""
        self.error += (
            "first name non only letters.\n" if not self.first_name.isalpha() else ""
        )

    def last_name_validate(self) -> None:
        """if last name has numbers or signs so add to error the explanation of the mistake."""
        self.error += (
            "last name non only letters.\n" if not self.last_name.isalpha() else ""
        )

    def id_validate(self) -> None:
        """if id has letters or signs so add to error the explanation of the mistake."""
        self.error += "id digits only.\n" if not self.id.isdigit() else ""
        self.error += (
            f"missing {9 - len(self.id)} numbers.\n" if len(self.id) < 9 else ""
        )
        self.error += (
            f"unnecessary {len(self.id) - 9} numbers.\n" if len(self.id) > 9 else ""
        )

    def phone_validate(self) -> None:
        """if phone has letters or signs so add to error the explanation of the mistake."""
        self.error += "phone digits only.\n" if not self.phone.isdigit() else ""
        self.error += (
            "phone with 10 numbers only.\n" if not len(self.phone) == 10 else ""
        )
        self.error += "phone starts with 0.\n" if not self.phone[0] == "0" else ""

    def dept_validate(self) -> None:
        """if dept has letters or signs except '-' in the left so add to error the explanation of the mistake."""
        wrong_letter = ""
        for letter in self.dept:
            if letter.isalpha() or letter in "~!@#$%^&*()_+`;:=[]}{\\|/?>,<":
                wrong_letter += letter
        if "-" in self.dept[1:]:
            wrong_letter += "-"
        self.error += (
            f"the letters '{wrong_letter}' not compatible." if wrong_letter else ""
        )

    def date_validate(self) -> None:
        """if date has letters so add to error the explanation of the mistake."""
        sep = ""
        for l in self.date:
            if not l.isalpha() and not l.isdigit():
                sep = l
                break
        date: list[str] = self.date.split(sep)
        self.error += f"day numbers only." if not date[0].isdigit() else ""
        self.error += f"month numbers only." if not date[1].isdigit() else ""
        self.error += f"year numbers only." if not date[2].isdigit() else ""
        try:
            day: int = int(date[0])
            month: int = int(date[1])
            year: int = int(date[2])
        except ValueError:
            return
        self.error += f"days only between 1 to 31." if not 1 <= day <= 31 else ""
        self.error += f"month only between 1 to 12." if not 1 <= month <= 12 else ""
        self.error += f"year only between 0 to 9999." if not 0 <= year <= 9999 else ""

    def checked(self) -> list[str]:
        """this run all tests and return errors or 'true' in list[str]"""
        self.first_name_validate()
        self.last_name_validate()
        self.id_validate()
        self.phone_validate()
        self.date_validate()
        self.dept_validate()
        if not self.error:
            return ["true"]
        return [self.error]
