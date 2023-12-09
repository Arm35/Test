from django.urls import path
from . import views

urlpatterns = [
    path('post', views.register),
    path('login', views.user_login),
    path('logout', views.logout_user),
    path('get', views.profile),
    path('category', views.getCategory),
    path('addtest',views.add_test),
    path('answer/<int:id>/', views.set_ture),
    path('gettest', views.get_test),
    path('del/<int:id>/', views.delete_test),
    path('test/<int:id>/', views.test_page),
    path('archive/<int:id>/', views.set_archive),
    path('get_id/<int:id>/', views.get_answer_id),
    path('api/add-rating/', views.add_rating, name='add-rating'),
    path('rating', views.user_rating),
    path('allratings', views.all_ratings),
    path('change_data/<int:test_id>/', views.change_test_data),
    path('change_name/<int:test_id>/', views.change_test_name, name='change_name'),
    path('change_question/<int:question_id>/', views.change_quastion, name='change_question'),
    path('change_answer/<int:answer_id>/', views.change_answer, name='change_answer'),
    path('change_category/<int:test_id>/', views.change_category, name='change_category'),

]
