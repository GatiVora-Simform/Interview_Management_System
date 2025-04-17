"""
URL configuration for ims project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [

    path('admin/', admin.site.urls),
    
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    path('api/', include('interview.api.urls')),
    path('api/', include('account.api.urls'))

]

'''
candidate token
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDkzNjQ0OCwiaWF0IjoxNzQ0ODY0NDQ4LCJqdGkiOiI2ZDMyNzFlNjc3MWI0MzE4OWYwNGU2MjRiZmVmZDBhZSIsInVzZXJfaWQiOjl9.DVhC0bSL128kUmtvFtBiDhPld2KyUi3p-Aj-ficd4VE",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1Mjk2NDQ4LCJpYXQiOjE3NDQ4NjQ0NDgsImp0aSI6IjMyYTFjODVhOGY1YzRlZmY5YzNhMWZhMjg0NjUyZTNiIiwidXNlcl9pZCI6OX0.7YCJvaNqmlQNXLHYtt15VPfsRdLOFE5ExLpTM2n5Hes"
}

interviewer2 token
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDkzNjg2NiwiaWF0IjoxNzQ0ODY0ODY2LCJqdGkiOiIxNDc2NmUwZmNlODQ0NDlmYTBkOTA1OGEzZjUxYTNiZiIsInVzZXJfaWQiOjExfQ.mjLq6TRuDn2aCOkCOTl1M7XDnm_Wix7zx8RgfFeV2Ac",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1Mjk2ODY2LCJpYXQiOjE3NDQ4NjQ4NjYsImp0aSI6IjQzY2E2ZDM2MzZiYjQ1ZGY4YmYyOWIzZTVkZWRkNWI3IiwidXNlcl9pZCI6MTF9.VkziVmxeGMep36aiVQYcJ4mzscsxCQGHVgNalFVbCow"
}

hr2 token
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDkzNzAyNSwiaWF0IjoxNzQ0ODY1MDI1LCJqdGkiOiJjZjU0MTljYmNhNzk0MTZkOGVmMTk2NTU4N2ExMGVhOCIsInVzZXJfaWQiOjEyfQ.1rzmb2HXfO96INc9M1ce5IR1ViXDHuInIZTJ4mv4_Xk",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1Mjk3MDI1LCJpYXQiOjE3NDQ4NjUwMjUsImp0aSI6ImJlZTg4ZjM5ZWE4ODRlYjVhMWM5NWJkZjVhMjlkYWExIiwidXNlcl9pZCI6MTJ9.J6QROf4dXg9PuprfSTHhCs_Fc2w-DJmM7dXZeEZ8SbE"
} 

'''


