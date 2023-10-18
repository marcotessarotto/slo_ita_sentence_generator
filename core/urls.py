from django.urls import path
from . import views

urlpatterns = [
    path('produce_examples/', views.produce_examples, name='produce_examples'),
]
