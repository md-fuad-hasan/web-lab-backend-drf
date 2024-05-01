from django.urls import path
from .views import Register,LoginView,DetailView,FormFillUpView,FormFillUpAllView,CourseView,FormFillUpCompleteView



urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', LoginView.as_view(), name="login"),
    path('personal-info/<id>/', DetailView.as_view(), name="detail"),
    path('form-fill-up/<id>/', FormFillUpView.as_view(), name="form-fill-up"),
    path('form-fill-up-all/<id>/', FormFillUpAllView.as_view(), name="form-fill-up-all"),
    path('course-detail/', CourseView.as_view(), name='course-detail'),
    path('form-fill-up-complete/<id>/',FormFillUpCompleteView.as_view(), name='form-fill-up-complete')

]