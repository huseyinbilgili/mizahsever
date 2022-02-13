from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.user.models import User
from apps.user.pipelines import UserCreatePipeline


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "first_name",
            "last_name",
            "date_of_birth",
            "email_allowed",
            "sms_allowed",
            "gender",
            "phone_number",
        )

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(dict(email=_("Email already taken.")))

    def create(self, validated_data):
        user = UserCreatePipeline(
            username=validated_data.get("username"),
            password=validated_data.get("password"),
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            date_of_birth=validated_data.get("date_of_birth"),
            email_allowed=validated_data.get("email_allowed"),
            sms_allowed=validated_data.get("sms_allowed"),
            gender=validated_data.get("gender"),
            phone_number=validated_data.get("phone_number"),
        ).run()
        return user
