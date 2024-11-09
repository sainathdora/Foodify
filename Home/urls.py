from django.urls import path
from . import views
urlpatterns=[
    path("", views.display, name='home'),
    # add home/ -> works for both www.domain.com/home & www.domain.com/home/
    path("upload/", views.upload_img, name="upload_image")
]