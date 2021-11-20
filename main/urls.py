from django.urls import path,include
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.homepage,name='home'),
    path('change/<int:id>', views.edit_book,name='change'),
    path('delete/<int:id>', views.delete,name='delete'),
    path('issue-book/<int:id>', views.issue_book,name='issuebook'),
    path('addbook', views.add_book,name='addbook'),
    path('booksissued', views.books_issued,name='booksissued'),
    path('all-books-issued', views.display_all_issued_books,name='all_books_issued'),
    path('returnbook/<int:id>', views.returnbook,name='returnbook'),
]
