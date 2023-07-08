from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name="home"),
    path('category/<slug:val>', views.CategoryView.as_view(), name="category"),
    path('search', views.SearchView.as_view(), name="search"),
    path('signup', views.SignupView.as_view(), name="signup"),
    path('signupSuccess', views.SignupSuccessView.as_view(), name="signupSuccess"),
    path('signin', views.SigninView.as_view(), name="signin"),
    path('profile', views.ProfileView.as_view(), name="profile"),
    path('changePwd', views.ChangePwdView.as_view(), name="changePwd"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)