import random
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from . models import Book, User
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.signing import TimestampSigner
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core import signing
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
import re

#custom methods

def is_six_digit_number(string):
    pattern = r'^\d{6}$'  # Matches a string consisting of exactly 6 digits
    return bool(re.match(pattern, string))

# Create your views here.
def home(request):
    user = User.objects.get(id=request.session.get('user_id')) if request.session.get('user_id') else None
    featuredBooks = Book.objects.filter(featured=True)
    topSellers = Book.objects.filter(topSeller=True)
    return render(request, "app/home.html", locals())

class CategoryView(View):
    def get(self, request, val):
        user = User.objects.get(id=request.session.get('user_id')) if request.session.get('user_id') else None
        book = Book.objects.filter(category=val)
        title = Book.objects.filter(category=val).values('title')
        category_name = Book.objects.filter(category=val).values('category')
        return render(request, "app/category.html", locals())

class SearchView(View):
    def get(self, request):
        user = User.objects.get(id=request.session.get('user_id')) if request.session.get('user_id') else None
        return render(request, "app/search.html", locals())
    
class SignupView(View):

    @staticmethod
    def encrypt(value):
        encrypted_value = signing.dumps(value)
        return encrypted_value
    
    def get(self, request):
        return render(request, "app/signup/signup.html", locals())
    
    def post(self, request):
        # Retrieve the form data from the POST request
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phonenumber = request.POST.get('phonenumber')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        card_number = self.encrypt(request.POST.get('card_number'))
        expiration_date = request.POST.get('expiration_date')
        security_code = self.encrypt(request.POST.get('security_code'))
        street_address = request.POST.get('street_address')
        apartment_suite = request.POST.get('apartment_suite')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        contact_phone = request.POST.get('contact_phone')
        contact_email = request.POST.get('contact_email')
        accept_terms = request.POST.get('accept_terms')
        
        # Check if passwords match
        if password != confirm_password:
            # Render the signup page with an error message
            return render(request, "app/signup/signup.html", {'password_mismatch': True})
        
        hashed_password = make_password(password)
        
        
        user = User(firstname=firstname, 
                    lastname=lastname, 
                    phonenumber=phonenumber, 
                    email=email,
                    password=hashed_password, 
                    card_number=card_number, 
                    expiration_date=expiration_date,
                    security_code=security_code, 
                    street_address=street_address,
                    apartment_suite=apartment_suite, 
                    city=city, 
                    state=state, 
                    zip_code=zip_code,
                    contact_phone=contact_phone, 
                    contact_email=contact_email,
                    accept_terms=accept_terms,
                    is_active=False
                    )


        signer = TimestampSigner()
        activation_token = signer.sign(email)  # Use the email as the token
        user.activation_token = activation_token
        user.save()

        # Prepare activation email
        activation_link = request.build_absolute_uri(
            reverse('activate_account', kwargs={'token': activation_token})
        )
        mail_subject = 'Activate your account'
        context = {
            'user': user,
            'activation_link': activation_link,
            'token': activation_token,  # Add the token variable to the context
        }
        message = render_to_string('app/signup/activation_email.html', context)

        # Send activation email
        send_mail(mail_subject, strip_tags(message), settings.DEFAULT_FROM_EMAIL, [email], html_message=message)
        
        # Redirect to the signup success page
        return render(request, "app/signup/signupSuccess.html", locals())

class SignupSuccessView(View):
    def get(self, request):
        user = User.objects.get(id=request.session.get('user_id')) if request.session.get('user_id') else None
        return render(request, "app/signup/signupSuccess.html", locals())
    
class SigninView(View):
    def get(self, request):
        user = User.objects.get(id=request.session.get('user_id')) if request.session.get('user_id') else None
        return render(request, "app/signin/signin.html", locals())
    
    def post(self, request):
        # Retrieve the form data from the POST request
        email_accountid = request.POST.get('email_accountid')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        if '@' in email_accountid:
            # If the provided value contains '@', treat it as an email
            user = User.objects.get(email=email_accountid)
        elif is_six_digit_number(str(email_accountid)):
            # Otherwise, treat it as an account ID
            user = User.objects.get(account_id=email_accountid)
        else:
            user = User.objects.get(firstname=email_accountid)

        if user is not None and user.check_password(password):
            if not user.is_active:
                print("done1")
                return render(request, "app/signin/accountSuspended.html", locals())
            elif user.is_admin:
                # Log in the user as an admin
                admin_user = authenticate(request, username=user.firstname, password=password)
                if admin_user is not None:
                    login(request, admin_user)
                    return HttpResponseRedirect(reverse('admin:index'))
                print("done2")
            else:
                print("loggedin")
                user.is_loggedin = True
                # Create a new session
                

                session = SessionStore()
                session['user_id'] = user.id
                if remember_me:
                    # Set the session expiry to a longer duration
                    session_expiry=session.set_expiry(604800)  # 7 days
                else:
                    # Set the session expiry to the default duration (using SESSION_COOKIE_AGE)
                    session_expiry=session.set_expiry(0)
                session.save()

                
                    

                # Set the session ID in the response cookies
                response = render(request, "app/signin/loginSuccess.html", locals())
                response.set_cookie('sessionid', session.session_key, session_expiry)

                # Redirect to the home page or any other desired page
                return response
        else:
            # Authentication failed
            return render(request, "app/signin/signin.html", {'auth_failed': True})
        
class LogoutView(View):
    def get(self, request):
        user = User.objects.get(id=request.session.get('user_id')) if request.session.get('user_id') else None
        # Get the user's session key
        session_key = request.COOKIES.get('sessionid')

        # Clear the session data
        Session.objects.filter(session_key=session_key).delete()

        # Update the is_loggedin field to False
        try:
            user = User.objects.get(id=request.user.id)
            user.is_loggedin = False
            user.save()
        except User.DoesNotExist:
            pass

        # Redirect to the desired page after logout
        return render(request, "app/signout/logoutSuccess.html", locals())
    
class ProfileView(View):
    @staticmethod
    def encrypt(value):
        encrypted_value = signing.dumps(value)
        return encrypted_value
    
    def decrypt(self, encrypted_value):
        decrypted_value = signing.loads(encrypted_value)
        return decrypted_value
    
    def get(self, request):
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id) if user_id else None
        user.card_number = self.decrypt(user.card_number)
        user.security_code = self.decrypt(user.security_code)
        return render(request, "app/profile/profile.html", {'user': user})
    
    def post(self, request):
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id) if user_id else None

        if user:
            # Update the user's information based on the submitted form data
            user.firstname = request.POST.get('firstname')
            user.lastname = request.POST.get('lastname')
            user.phonenumber = request.POST.get('phonenumber')
            user.email = request.POST.get('email')
            user.card_number = self.encrypt(request.POST.get('card_number'))
            user.expiration_date = request.POST.get('expiration_date')
            user.security_code = self.encrypt(request.POST.get('security_code'))
            user.street_address = request.POST.get('street_address')
            user.apartment_suite = request.POST.get('apartment_suite')
            user.city = request.POST.get('city')
            user.state = request.POST.get('state')
            user.zip_code = request.POST.get('zip_code')
            user.contact_phone = request.POST.get('contact_phone')

            # Save the updated user object
            user.save()
            mail_subject = 'Profile Updated'
            context = {
            'user': user,
            }
            message = render_to_string('app/profile/profile_update_success.html', context)

            # Send the email with the user_id
            send_mail(mail_subject, strip_tags(message), settings.DEFAULT_FROM_EMAIL, [user.email])

        return render(request, "app/profile/edit_profile_success.html", {'user': user})
    
    
    
class ChangePwdView(View):
    def get(self, request):
        user = User.objects.get(id=request.session.get('user_id')) if request.session.get('user_id') else None
        return render(request, "app/change_password/changePwd.html", locals())
    
    def post(self, request):
        old_password = request.POST.get('oldPassword')
        new_password1 = request.POST.get('newPassword1')
        new_password2 = request.POST.get('newPassword2')

        # Retrieve the user based on the session ID
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id) if user_id else None
        print(user)

        if user:
            # Check if the old password matches the user's current password
            if user.check_password(old_password):
                # Validate the new password
                if new_password1 == new_password2:
                    # Set the user's new password
                    user.password = make_password(new_password1)
                    user.save()
                    print("changed")
                    
                    return render(request, "app/change_password/chgPwdSuccess.html", locals())  # Redirect to the profile page or any other desired page
                else:
                    return render(request, "app/change_password/changePwd.html", {'match_failed': True})
            else:
                print('old wrong pwd')
        else:
            print('user nf')

        return render(request, "app/change_password/changePwd.html", {'check_failed': True})
    

class BookDetailsView(View):
    def get(self, request, book_isbn):
        user = User.objects.get(id=request.session.get('user_id')) if request.session.get('user_id') else None
        book = get_object_or_404(Book, ISBN=book_isbn)
        return render(request, "app/bookDetails.html", locals())
    
class CartView(View):
    def get(self, request):
        user = User.objects.get(id=request.session.get('user_id')) if request.session.get('user_id') else None
        return render(request, "app/order/cart.html", locals())

class CheckoutView(View):
    def get(self, request):
        user = User.objects.get(id=request.session.get('user_id')) if request.session.get('user_id') else None
        return render(request, "app/order/checkout.html", locals())

class OrderSummaryView(View):
    def get(self, request):
        user = User.objects.get(id=request.session.get('user_id')) if request.session.get('user_id') else None
        return render(request, "app/order/orderSummary.html", locals())
    
class OrderSuccessView(View):
    def get(self, request):
        user = User.objects.get(id=request.session.get('user_id')) if request.session.get('user_id') else None
        return render(request, "app/order/orderSuccess.html", locals())
    
class OrderHistoryView(View):
    def get(self, request):
        user = User.objects.get(id=request.session.get('user_id')) if request.session.get('user_id') else None
        return render(request, "app/order/orderHistory.html", locals())
    

def activate_account(request, token):
    try:
        user = User.objects.get(activation_token=token)
    except User.DoesNotExist:
        user = None

    if user is not None:
        user.is_active = True
        user.activation_token = None
        user.save()

        # Prepare the email with the user_id
        mail_subject = 'Your Account ID'
        message = render_to_string('app/profile/user_id_email.html', {
            'account_id': user.account_id,
        })

        # Send the email with the user_id
        send_mail(mail_subject, strip_tags(message), settings.DEFAULT_FROM_EMAIL, [user.email])

        return render(request, 'app/signup/account_activated.html')
    
    return render(request, "app/signup/activation_error.html")

class FpEnterEmailView(View):
    def get(self, request):
        return render(request, "app/forgot_password/Fp_Enter_Email.html", locals())
    
    def post(self, request):
        # Retrieve the form data from the POST request
        email = request.POST.get('reset_email')

        #OTP Generator
        reset_token = random.randint(100000, 999999)

        user = User.objects.get(email=email)
        print(user)
        user.reset_token = reset_token
        print(user.reset_token)
        user.save()

        mail_subject = 'Reset your password'
        context = {
            'user': user,
            'token': reset_token,  # Add the token variable to the context
        }
        message = render_to_string('app/forgot_password/Reset_Link_email.html', context)

        # Send activation email
        send_mail(mail_subject, strip_tags(message), settings.DEFAULT_FROM_EMAIL, [email], html_message=message)
        
        # Redirect to the signup success page
        return redirect('ResetPassword')
    
class reset_account(View):
    def get(self, request):
        return render(request, "app/forgot_password/reset_password.html", locals())
    
    def post(self, request):
        validate_token = request.POST.get('otp')
        new_password1 = request.POST.get('password1')
        new_password2 = request.POST.get('password2')
        try:
            user = User.objects.get(reset_token=validate_token)
        except User.DoesNotExist:
            user = None

        if user is not None and new_password1==new_password2:
            user.reset_token = None
            user.password=make_password(new_password1)
            user.save()

            # Prepare the email with the user_id
            mail_subject = 'Password Changed'
            message = render_to_string('app/forgot_password/password_reset_success.html')

            # Send the email with the user_id
            send_mail(mail_subject, strip_tags(message), settings.DEFAULT_FROM_EMAIL, [user.email])

            return render(request, 'app/forgot_password/reset_password_success.html')
        
        return render(request, "app/forgot_password/reset_password_error.html")

# class ResetPasswordView(View):

#     def get(self, request, email):
#         # Use the email to retrieve the user
#         user = User.objects.get(email=email)
#         return render(request, "app/reset_password.html", {'email': email, 'user': user})
    
#     def post(self, request):
#         new_password1 = request.POST.get('password1')
#         new_password2 = request.POST.get('password2')

#         # Retrieve the user based on the session ID
#         user_id = request.session.get('user_id')
#         user = User.objects.get(id=user_id) if user_id else None
#         print(user)

#         if user:
#             # Check if the old password matches the user's current password
#             if user.check_password(old_password):
#                 # Validate the new password
#                 if new_password1 == new_password2:
#                     # Set the user's new password
#                     user.password = make_password(new_password1)
#                     user.save()
#                     print("changed")
                    
#                     return render(request, "app/change_password/chgPwdSuccess.html", locals())  # Redirect to the profile page or any other desired page
#                 else:
#                     return render(request, "app/change_password/changePwd.html", {'match_failed': True})
#             else:
#                 print('old wrong pwd')
#         else:
#             print('user nf')

#         return render(request, "app/change_password/changePwd.html", {'check_failed': True})
