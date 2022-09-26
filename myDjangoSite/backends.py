from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        userModel = get_user_model()
        print(userModel)
        try:
            user = userModel.objects.get(email=username)
            if user is None:
                return None
            if user.check_password(password):
                return user
        except:
            return None
