from django.utils import timezone

from apps.user.models import User


class UserCreatePipeline:
    def __init__(
        self,
        username,
        password,
        email,
        first_name,
        last_name,
        date_of_birth,
        email_allowed,
        sms_allowed,
        gender,
        phone_number,
    ):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email_allowed = email_allowed
        self.sms_allowed = sms_allowed
        self.gender = gender
        self.phone_number = phone_number
        self._user = None

    @property
    def user(self):
        return self._user

    def create(self):
        self._user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            date_of_birth=self.date_of_birth,
            email_allowed=self.email_allowed,
            sms_allowed=self.sms_allowed,
            gender=self.gender,
            phone_number=self.phone_number,
            last_login=timezone.now(),
        )

    def run(self):
        self.create()
        return self.user
