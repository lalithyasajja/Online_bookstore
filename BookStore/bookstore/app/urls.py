from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('category/<slug:val>', views.CategoryView.as_view(), name="category"),
    path('search', views.SearchView.as_view(), name="search"),
    path('signup', views.SignupView.as_view(), name="signup"),
    path('fPEnterEmail', views.FpEnterEmailView.as_view(), name="fPEnterEmail"),
    path('ResetPassword', views.reset_account.as_view(), name='ResetPassword'),
    path('activate/<str:token>/', views.activate_account, name='activate_account'),
    path('signupSuccess', views.SignupSuccessView.as_view(), name="signupSuccess"),
    path('signin', views.SigninView.as_view(), name="signin"),
    path('profile', views.ProfileView.as_view(), name="profile"),
    path('checkout', views.CheckoutView.as_view(), name="checkout"),
    path('orderSummary', views.OrderSummaryView.as_view(), name="orderSummary"),
    path('orderSuccess', views.OrderSuccessView.as_view(), name="orderSuccess"),
    path('orderHistory', views.OrderHistoryView.as_view(), name="orderHistory"),
    path('changePwd', views.ChangePwdView.as_view(), name='change_password'),
    path('bookDetails/<slug:book_isbn>', views.BookDetailsView.as_view(), name="bookDetails"),
    path('cart', views.CartView.as_view(), name="cart"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)