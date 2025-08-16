import re
from django.contrib.auth.models import User

def is_email_unique(email):
    return not User.objects.filter(email=email).exists()

def check_password_strength(password):
    if len(password) < 8:
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    return True