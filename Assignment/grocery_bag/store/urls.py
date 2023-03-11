from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='homepage'),
    # path('bloghome',views.blogHome,),
    path('updateitem/<int:pk>',views.ItemUpdateView.as_view(success_url="/")),
    path('deleteitem/<int:pk>',views.deleteView),
    path('signup',views.signup),
    path('logout',views.logout),
    path('login',views.login),
    path('item',views.ItemListView.as_view()),
    path('search',views.searchView),
    path('youritem',views.your_item),
    path('createitem',views.ItemCreateView.as_view(success_url="/")),
]
