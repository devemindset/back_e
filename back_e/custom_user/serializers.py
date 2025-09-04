from rest_framework import serializers
from .models import CustomUser,UserSubscription,UserVerification
from django.contrib.auth import get_user_model, login as auth_login, authenticate
from projects.serializers import ProjectLightSerializer




User = get_user_model()

MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 MB
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "code"]

    def create(self, validated_data):
        # On ne stocke pas le code
        validated_data.pop("code", None)
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_verified=True,
        )

class BeforeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVerification
        fields = "__all__"

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        request = self.context.get("request")
        email = data.get("email")
        password = data.get("password")

        user = authenticate(request,email=email,password=password)

        if not user: 
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("User account is desabled")
        if user.is_verified == False:
            raise serializers.ValidationError("This account has not been verified.")
        
        
        auth_login(request,user)


        data["user"] = user 
        return data

        
class GoogleAuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    social_id = serializers.CharField()
    social_image = serializers.URLField(required=False)

    def validate(self, data):
        return data



class CustomUserSerializer(serializers.ModelSerializer):

    class Meta: 
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "auth_provider",
            "social_image",
            "is_social_account",
            "created_at",

        ]

    def validate_username(self, value):
        # Si le username a changé
        if self.instance and self.instance.username != value:
            if User.objects.filter(username=value).exists():
                raise serializers.ValidationError("This username is already taken.")
        return value
    
    def validate(self, data):
        return data
    
    # def validate_image(self, image):
    #     if image.size > MAX_IMAGE_SIZE:
    #         raise serializers.ValidationError("Profile image must be under 2MB.")
    #     if image.content_type not in ALLOWED_IMAGE_TYPES:
    #         raise serializers.ValidationError("Only JPEG, PNG and WEBP images are allowed.")
    #     return image

    # def validate_branding_image(self, image):
    #     if image.size > MAX_IMAGE_SIZE:
    #         raise serializers.ValidationError("Branding image must be under 2MB.")
    #     if image.content_type not in ALLOWED_IMAGE_TYPES:
    #         raise serializers.ValidationError("Only JPEG, PNG and WEBP images are allowed.")
    #     return image

    # def validate_branding_background(self, image):
    #     if image.size > MAX_IMAGE_SIZE:
    #         raise serializers.ValidationError("Branding background must be under 2MB.")
    #     if image.content_type not in ALLOWED_IMAGE_TYPES:
    #         raise serializers.ValidationError("Only JPEG, PNG and WEBP images are allowed.")
    #     return image


      
class UserFeedbackSerializer(serializers.Serializer):
    name = serializers.CharField(required=True,max_length=10)
    message = serializers.CharField(required=True,max_length=1000)
    recaptcha_token = serializers.CharField(required=True)
    

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    message = serializers.CharField(required=True,max_length=1000)
    recaptcha_token = serializers.CharField(required=True)