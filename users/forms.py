from django.contrib.auth.forms import UserCreationForm

import users

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = users
        fields = ['username', 'email','password']