from django.urls import path
from . import views


urlpatterns = [
    path('stadiums/', views.StadiumView.as_view()),
    path('stadium/<int:pk>/', views.StadiumDetailView.as_view()),
    path('stadium-update/<int:pk>/', views.StadiumUpdateView.as_view()),
    path('stadiums/filter/', views.StadiumsFilter.as_view()),
    path('stadims/filter/owner/<int:pk>/', views.FilterStadiumsByOwner.as_view()),
    
    path('books/', views.BookView.as_view()),
    path('book-cancel/<int:pk>/',views.BookCancelView.as_view()),
    path('book-create/',views.BookCreateView.as_view()),

    path('owners/', views.OwnerListView.as_view()),
    path('users/', views.UserListView.as_view()),
    path('owner-detail/<int:pk>/', views.OwnerDetailView.as_view()),
    path('user-detail/<int:pk>/', views.UserDetailView.as_view()),
]