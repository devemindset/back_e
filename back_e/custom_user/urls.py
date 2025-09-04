from django.urls import path
from .views import register_user,login_user,google_auth,user_action,feed_back_view,user_info,logout_user,contact_form,upgrade_plan_view,update_user_view,delete_user_view,sendgrid_test_view,BeforeRegisterAPIView


urlpatterns = [
    path('track-action/', user_action, name='track-action'),
    path("feedback/",feed_back_view),
    path("register_user/",register_user),
    path("login_user/",login_user),
    path("delete/<int:pk>/delete_user_view",delete_user_view),
    path("google_auth/",google_auth),

    path("user_info/",user_info),
    path("logout/", logout_user, name="logout"),
    path("upgrade_plan_view/",upgrade_plan_view),
    path("contact_form/",contact_form),
     path("user_update/",update_user_view),
     path("test-sendgrid/", sendgrid_test_view),
     path("before_register/",BeforeRegisterAPIView.as_view())

]