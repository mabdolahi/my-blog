from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('' , views.index , name = 'index'),
    path('postlist/' , views.postlist , name = 'post_list'),
    path('postdetail/<slug:slug>/' , views.postdetail , name = 'post_detail'),
    path('account-form/' , views.UserAccount , name = 'account_form'),
    path('signup/', views.Signup, name='signup'),

]
