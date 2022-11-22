from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('requestbook', views.requestbook, name='requestbook'),
    path('displayrequest', views.requestedbooks, name='requestedbooks'),
    path('displayrequest', views.requestedbooks, name='requestedbooks'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('book_search', views.book_search, name='book_search'),
    # urlpatterns for messaging.
    path('book_detail', views.contact, name='contact'),
    path('mymessages', views.mymessages, name='mymessages'),
    path('sendmessage', views.sendmessage, name='sendmessage'),
    path('message_delete/<int:message_id>', views.message_delete, name='message_delete'),
    path('message_reply/<int:message_id>', views.message_reply, name='message_reply'),
    path('message_reply', views.reply, name='reply'),

]