from django.urls import path
from . import views

urlpatterns = [
    path('produce_examples/', views.produce_examples, name='produce_examples'),
    path('produce_slo_ita_example/', views.produce_slo_ita_example, name='produce_slo_ita_example'),

    path('', views.homepage, name='homepage'),
]
