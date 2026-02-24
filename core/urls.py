from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Maps the root URL of the app to the 'index' view
path('generate-questions/', views.generate_questions_view, name='generate_questions'),
]