from django.shortcuts import render
from rest_framework import generics,status,views
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from django.contrib.auth import get_user_model,logout,login as auth_login
from .serializers import CustomUserSerializer,RegisterSerializer,LoginSerializer,GoogleAuthSerializer,UserFeedbackSerializer,EmailSerializer,BeforeRegisterSerializer,CustomerInfoSerializer
from django.middleware.csrf import get_token
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import UserAction,UserFeedback,ContactForm,UserVerification,CustomerInfo
from decouple import config
import requests
from django.conf import settings

from django.utils import timezone
from datetime import timedelta
from tools.validators import generate_verification_code


User = get_user_model()

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data, context={"request": request})

        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get("email")
        code = serializer.validated_data.get("code")

        user_verify = UserVerification.objects.filter(verification_code=code).first()

        # Vérifications
        if not user_verify:
            return Response({"error": "No verification code found for this email."}, status=status.HTTP_404_NOT_FOUND)

        if user_verify.verification_code != code:
            return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)

        if not user_verify.code_expiration or timezone.now() > user_verify.code_expiration:
            return Response({"error": "Verification code has expired."}, status=status.HTTP_400_BAD_REQUEST)

        # Création de l'utilisateur
        try:
            user = serializer.save()
            user_verify.delete()
            auth_login(request, user)
            request.session.modified = True  # 🔑 Force la session (nécessaire pour envoyer sessionid)
            #welcome mail
            # welcome_notification_email(user.email)

            # Réponse
            response = Response({
                "message": "Register successful",
                "csrf_token": get_token(request)
            }, status=status.HTTP_201_CREATED)

            cookie_params = {
                "key": "auth_status",
                "value": "true",
                "httponly": False,
                "secure": not settings.DEBUG,
                "samesite": "None" if not settings.DEBUG else "Lax",
            }

            if not settings.DEBUG:
                cookie_params["domain"] = settings.SESSION_COOKIE_DOMAIN

            response.set_cookie(**cookie_params)
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
register_user = RegisterView.as_view()

class BeforeRegisterAPIView(APIView):
   

    def post(self, request):
        serializer = BeforeRegisterSerializer(data=request.data)
   
        if serializer.is_valid():

            email = serializer.validated_data["email"]
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            verification_code = generate_verification_code()
            code_expiration = timezone.now() + timedelta(minutes=15)
         

            if User.objects.filter(email=email).exists():
                return Response({"error" : "A user with this email already exists"}, status=status.HTTP_409_CONFLICT)
            
            if User.objects.filter(username=username).exists():
                return Response({"error" : "A user with this username already exists"}, status=status.HTTP_409_CONFLICT)

            try:
                UserVerification.objects.create(
                    username=username,
                    email=email,
                    password=password,
                    verification_code=verification_code,
                    code_expiration=code_expiration,
                )

             
                # send_verification_email(email=email,code=verification_code)
                # website_action_message("New register","down time note")

                return Response({
                        "message" : "successfully"
                    ,
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                print("error",str(e))
                return Response({"error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})

        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]

        if user:
            auth_login(request, user)
         
            response = Response({
                "message": "Login successful",
                "csrf_token": get_token(request)
            }, status=status.HTTP_200_OK)

            # Définir les attributs dynamiquement selon l’environnement
            cookie_params = {
                "key": "auth_status",
                "value": "true",
                "httponly": False,
                "secure": not settings.DEBUG,
                "samesite": "None" if not settings.DEBUG else "Lax",
            }

            if not settings.DEBUG:
                cookie_params["domain"] = settings.SESSION_COOKIE_DOMAIN

            response.set_cookie(**cookie_params)

            return response
        
login_user = LoginView.as_view()

class LogoutView(views.APIView):
    permission_classes = []

    def post(self, request):
        logout(request)

        response = Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)

        cookie_domain = settings.SESSION_COOKIE_DOMAIN if not settings.DEBUG else None

        response.delete_cookie("sessionid", domain=cookie_domain)
        response.delete_cookie("csrftoken", domain=cookie_domain)
        response.delete_cookie("auth_status", domain=cookie_domain)

        return response
    
    
logout_user = LogoutView.as_view()

class GoogleAuthView(generics.GenericAPIView):
    serializer_class = GoogleAuthSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        social_image = serializer.validated_data["social_image"]
        username = serializer.validated_data["username"]
        social_id = serializer.validated_data["social_id"]

        user = User.objects.filter(username=username, email=email).first()
        is_new_user = False

        if user:
            # ✅ Login direct
            auth_login(request, user)
        else:
            # ⚙️ Génère un nom unique si nécessaire
            if User.objects.filter(username=username).exclude(email=email).exists():
                base_name = username
                counter = 1
                while User.objects.filter(username=f"{base_name}_{counter}").exists():
                    counter += 1
                username = f"{base_name}_{counter}"

            # 🆕 Création de l'utilisateur
            user = User.objects.create(
                username=username,
                email=email,
                social_id=social_id,
                social_image=social_image,
                is_social_account=True,
                auth_provider="google"
            )
            is_new_user = True
            auth_login(request, user)
            #welcome mail
            # welcome_notification_email(user.email)
            # website_action_message("register","back e")

        # ✅ Réponse + Cookie
        response = Response({
            "message": "Signup successful" if is_new_user else "Login successful",
            "csrf_token": get_token(request)
        }, status=status.HTTP_200_OK)

        # 💡 Adaptatif prod/dev
        cookie_params = {
            "key": "auth_status",
            "value": "true",
            "httponly": False,
            "secure": not settings.DEBUG,
            "samesite": "None" if not settings.DEBUG else "Lax",
        }

        if not settings.DEBUG:
            cookie_params["domain"] = settings.SESSION_COOKIE_DOMAIN

        response.set_cookie(**cookie_params)

        return response
        
google_auth = GoogleAuthView.as_view()
      
class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated :
            user = request.user
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail" : "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

user_info = UserInfoView.as_view()

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_user_view(request):
    serializer = CustomUserSerializer(request.user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    # Détection automatique des champs en erreur
    field_errors = list(serializer.errors.keys())

    # Message par défaut
    message = "Invalid data submitted."


    if "username" in field_errors:
        message = "Invalid username. Please check length and uniqueness."
    elif "email" in field_errors:
        message = "Invalid email format or already in use."

    return Response(
        {
            "errors": serializer.errors,
            "message": message,
        },
        status=status.HTTP_400_BAD_REQUEST
    )

class DestroyUserAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()

        if request.user != user and not request.user.is_staff:
            return Response({
                "detail": "Not authorized"
            }, status=status.HTTP_403_FORBIDDEN)

        # Supprimer l'utilisateur
        self.perform_destroy(user)

        # Déconnecter et supprimer la session
        logout(request)

        response = Response({
            "detail": "User deleted successfully"
        }, status=status.HTTP_200_OK)

        # ✅ Supprimer les cookies avec le bon `domain` en prod
        cookie_domain = settings.SESSION_COOKIE_DOMAIN if not settings.DEBUG else None

        response.delete_cookie("sessionid", domain=cookie_domain)
        response.delete_cookie("csrftoken", domain=cookie_domain)
        response.delete_cookie("auth_status", domain=cookie_domain)

        return response

delete_user_view = DestroyUserAPIView.as_view()

# ----------------user action and feedback ------------------------

class UserActionView(APIView):
    def post(self, request):
        object = request.data.get('object')
        action = request.data.get('action')


        UserAction.objects.create(
                action=action,
                object=object,
            )

        return Response({"message": "Action recorded"}, status=status.HTTP_201_CREATED)

user_action = UserActionView.as_view()

class UserFeedbackView(generics.GenericAPIView):
    serializer_class = UserFeedbackSerializer

    def post(self,request, *args,**kwargs):
        serializer = self.get_serializer(data=request.data,context={"request": request})
        if not serializer.is_valid():
            return Response({"errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST 
                            )
        name = serializer.validated_data["name"]
        message = serializer.validated_data["message"]
        recaptcha_token = serializer.validated_data["recaptcha_token"]

        # verify reCAPTCHA with Google
        recaptcha_response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret" : config("RECAPTCHA_SECRET_KEY",default=""),
                "response" : recaptcha_token
            }
        ).json()

        # check if verification was successful
        if not recaptcha_response.get("success"):
            return Response({"error" : "reCAPTCHA verification failed"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            UserFeedback.objects.get_or_create(
                name = name,message=message
            )
            # forward_contact_message(f"{name } feedback",message)
            return Response({
                "message" : "Feedback submitted successfully"
            },status=status.HTTP_201_CREATED)
        
        except Exception as e:
                print("error",str(e))
                return Response({"error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
feed_back_view = UserFeedbackView.as_view()

class ContactFormView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data["email"]
            user_message = serializer.validated_data["message"]
            recaptcha_token = request.data.get("recaptcha_token")

            # verify reCAPTCHA with Google
            recaptcha_response = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={
                    "secret" : config("RECAPTCHA_SECRET_KEY",default=""),
                    "response" : recaptcha_token
                }
            ).json()

            # check if verification was successful
            if not recaptcha_response.get("success"):
                return Response({"error" : "reCAPTCHA verification failed"},status=status.HTTP_400_BAD_REQUEST)
            
            try:
                # Send the email via Mailersend
                # send_contact_email(user_email=user_email,user_message=user_message)
                # forward_contact_message(user_email,user_message)
                email_send_from_contact,created = ContactForm.objects.get_or_create(email=user_email,message=user_message)
                if created:
                    return Response({"message": "Email sent succesfully"},status=status.HTTP_200_OK)
            except Exception as e:
                print("error",str(e))
                return Response({"error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
contact_form = ContactFormView.as_view()




class CustomerInfoAPIView(APIView):
    def post(self, request):
        serializer = CustomerInfoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        full_name = serializer.validated_data.get("full_name", "")
        phone = serializer.validated_data.get("phone", "")

        try:
            CustomerInfo.objects.create(
                email=email,phone=phone, full_name=full_name
            )
            
            return Response({"message" : "success"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)