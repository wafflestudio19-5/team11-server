from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _, ngettext
import re

class MaximumLengthValidator:
    def __init__(self, max_length = 20):
        self.max_length = max_length
    
    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                ngettext(
                    "This password is too long. It must contain at most %(max_length)d character", "This password is too long. It must contain at most %(max_length)d characters", self.max_length
                ),
                code='password_too_long',
                params={'max_length' : self.max_length}
            )

class PasswordFormValidator:
    def validate(self, password, user=None):
        num = 0
        
        regex = "[A-Za-z]+"
        p = re.compile(regex)
        result = p.search(password)
        if result != None:
            num += 1
        
        regex = "\d+"
        p = re.compile(regex)
        result = p.search(password)
        if result != None:
            num += 1
        
        regex = "[@$!%*^#&]+"
        p = re.compile(regex)
        result = p.search(password)
        if result != None:
            num += 1
        
        if num < 2:
            raise ValidationError("This password format is wrong")