from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, first_name=None, last_name=None, is_staff=False, is_superuser=False):
        if not email or not password:
            raise ValueError('Please, provide correct Email and Password')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, is_staff=is_staff,
                          is_superuser=is_superuser)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, first_name=None, last_name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("'is_staff' must be set True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("'is_superuser' must be set True")

        return self.create_user(email, password, first_name, last_name, **extra_fields)
