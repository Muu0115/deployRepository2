from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from myapp import views
from myapp.views import home, SignUpView, manage_health_record, health_record, add_weblink, guestbook

    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login/login.html'), name='login'),
    path('signup/', SignUpView.as_view(template_name='signup/signup.html'), name='signup'), 
    path('', home, name='home'),
    path('home/', views.home, name='home'),
    path('health_record/<int:year>/<int:month>/<int:day>/', manage_health_record, name='manage_health_record'),
    path('health_record/<int:year>-<int:month>-<int:day>/', views.health_record, name='health_record'),
    path('weblink/add/', add_weblink, name='add_weblink'),  
    path('guestbook/', guestbook, name='guestbook'),
    path('my_page/', views.mypage, name='my_page'), 
    path('web-links/', views.weblink_list, name='weblink_list'),
    path('web-links/<int:pk>/', views.weblink_detail, name='weblink_detail'),
]
