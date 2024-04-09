from django.urls import path
from myapp.views import BookList, BookDetail
from myapp.views import *
from myapp.views import StudentGeneric

urlpatterns = [

    path('generic-student/', StudentGeneric.as_view()),
    path('generic-student/<id>/', StudentGeneric1.as_view()),

    path('crud_django/', BookList.as_view()),
    path('crud_django/<str:pk>/', BookDetail.as_view())
]