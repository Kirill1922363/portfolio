from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('projects/',views.projects,name='projects'),
    path('projects/<int:pk>/',views.project_detail,name='project_detail'),
    path('pricing/',views.pricing, name='pricing'),
    path('pricing/success/',views.pricing_success,name='pricing_success'),
    path('api/calculate/',views.calculate_price, name='calculate_price'),
    path('blog/',views.blog_list,name='blog_list'),
    path('blog/<slug:slug>/',views.blog_detail,name='blog_detail'),
    path('contact/', views.contact,name='contact'),
    path('analytics/',views.analytics,name='analytics'),
]
