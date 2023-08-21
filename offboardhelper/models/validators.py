#from InquirerPy import (ValidationError, Validator)
from prompt_toolkit.validation import ValidationError, Validator
import re

class EmailValidator(Validator):
    pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"

    def validate(self, email):
        if len(email.text):
            if re.match(self.pattern, email.text):
                return True
            else:
                raise ValidationError(
                    message="Invalid email",
                    cursor_position=len(email.text))
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(email.text))
            
class EmptyValidator(Validator):
    def validate(self, value):
        if len(value.text):
            return True
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))

class TicketValidator(Validator):
    def __init__(self, message: str = "Input cannot be empty") -> None:
        self._message = message

    def validate(self, document) -> None:
        
        """Check if user input is empty. and if it matches Autotask's Ticket format

        This method is used internally by `prompt_toolkit <https://python-prompt-toolkit.readthedocs.io/en/master/>`_.

        See Also:
            https://python-prompt-toolkit.readthedocs.io/en/master/pages/asking_for_input.html?highlight=validator#input-validation
        """
        if not len(document.text) > 0:
            raise ValidationError(
                message=self._message,
                cursor_position=document.cursor_position,
            )
        else:
            pattern = r'^T\d{4}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])\.\d{4}$'
            if re.match(pattern, document.text):
                # FIXME add function to validate agasint the Autotask
                return True
            else:
                raise ValidationError(
                    message="Invalid ticket format",
                    cursor_position=len(document.text))

        
