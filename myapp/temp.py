from myapp.models import User
from django.shortcuts import get_object_or_404

# Assuming you have the user_id of the User instance you want to delete
user_id_to_delete = 14  # Replace with the actual user_id

# Get the User instance
user_to_delete = get_object_or_404(User, id=user_id_to_delete)

# Delete the User instance and associated profiles
user_to_delete.delete()

