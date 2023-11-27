from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Since 'username' in the form is treated as the email.
            user = User.objects.get(email=username)
            print(user)
            if user.check_password(password) and self.user_can_authenticate(user):
                # Check if the user has the admin role.
                if user.role == 'admin':  # Make sure to use the correct role string as per your model definition
                    print(user)
                    return user
        except User.DoesNotExist:
            # Run the default password hasher once to reduce timing
            # difference between an existing and a non-existing user.
            User().set_password(password)
        return None
