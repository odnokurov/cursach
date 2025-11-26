#from django.urls import path
#from . import views
#from django.conf.urls import url

#urlpatterns = [
#    url(r'^$', views.index, name='index'),
#    url(r'^books/$', views.BookListView.as_view(), name='books'),
#    url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
#]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]
urlpatterns += [
    path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]