from django.contrib import admin
from django.urls import path
from core.views import home, login_view, signup_view, dashboard, study_materials, biology, chemistry, physics,  analytics, wellbeing, mock_tests, start_test, profile, edit_profile, chatbot

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", home, name="home"),

    path("login/", login_view, name="login"),

    path("signup/", signup_view, name="signup"),

    path("dashboard/", dashboard, name="dashboard"),

    path("study-materials/", study_materials, name="study_materials"),

    path("biology/", biology, name="biology"),

    path("chemistry/", chemistry, name="chemistry"),

    path("physics/", physics, name="physics"),

    path("analytics/", analytics, name="analytics"),

    path("well-being/", wellbeing, name="wellbeing"),

    path("mock-tests/", mock_tests, name="mock_tests"),

    path("test/", start_test, name="start_test"),

    path("profile/", profile, name="profile"),

    path("profile/edit/", edit_profile, name="edit_profile"),

    path("chatbot/", chatbot, name="chatbot"),
]