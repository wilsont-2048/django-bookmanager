from django.db.models import Q

from .models import MainMenu
from .models import Book, RequestBook
from .forms import RequestBookForm
from .forms import BookForm
from .forms import ReviewForm
from .forms import SearchForm

from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView

from .forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Messaging Stuff
from .models import Message
from .forms import RequestBookForm, MessageForm

# Use User auth table for username info
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    # return HttpResponse("Hello World")
    return render(request, 'bookMng/home.html',{
        'item_list': MainMenu.objects.all()
    })


def home(request):
    return render(request, 'home.html')

@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    form = SearchForm()
    sellBook = BookForm()
    books = book_search(request)
    try:
        for b in books:
            b.pic_path = b.picture.url[19:]
    except Exception:
        return HttpResponseRedirect('/displaybooks')
    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                      'form': form,
                      'sellBook': sellBook,
                  })


@login_required(login_url=reverse_lazy('login'))
def book_search(request):
    query = request.POST.get('searchbar', '')
    if query:
        queryset = Q(name__icontains=query)
        results = Book.objects.filter(queryset).distinct()
        print(f'book_search: Returning results for {query}')
        return results
    else:
       return Book.objects.all()


@login_required(login_url=reverse_lazy('login'))
def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })


@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = Book.objects.filter(user_name=request.user) # like database select
    for b in books:
        b.pic_path = b.picture.url[19:]
    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })


@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                book.user_name = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/displaybooks')
        else: # If the form fails, go back to display book
            return displaybooks(request)
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True

@login_required(login_url=reverse_lazy('login'))
def requestedbooks(request):
    requestbooks = RequestBook.objects.all()
    for rb in requestbooks:
        return render(request, 'bookMng/displayrequest.html', {
            'requestedbooks': requestbooks
        })

@login_required(login_url=reverse_lazy('login'))
def requestbook(request):
    submitted = False
    if request.method == 'POST':
        form = RequestBookForm(
            request.POST
        )
        if form.is_valid():
            request_book = form.save(commit=False)
            request_book.save()
            return HttpResponseRedirect('/displayrequest')
        else:
            return requestedbooks(request)
    else: # If the form fails, go back to requested books
        form = RequestBookForm()
        if 'submitted' in request.GET:
            submitted = True

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
            'form': form
    })


@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[19:]
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            if 1 <= review.rating <= 5:
                try:
                    review.book = book
                    review.username = request.user
                except Exception:
                    pass
                review.save()
            return HttpResponseRedirect(f'/book_detail/{book_id}')
    else:
        form = ReviewForm()
    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  })


# Definitions used for messaging.
def contact(request):
    if request.method == "POST":
        newmessage = Message()
        post_username = request.POST['post-username']
        subject = request.POST['subject']
        message = request.POST['message']

        newmessage.sender = request.user
        try:
            newmessage.receiver = User.objects.get(username=post_username)
        except: # If the user does not exist in the database, go back to the displayrequested books page (or whatever)
            return requestedbooks(request)
        newmessage.subject = subject
        newmessage.message = message

        newmessage.save()

        return render(request, 'bookMng/displaybooks.html',
                      {'message_sender': newmessage.sender, 'message_receiver': newmessage.receiver})
    else:
        return render(request, 'bookMng/displaybooks.html', {})

@login_required(login_url=reverse_lazy('login'))
def mymessages(request):
    messages = Message.objects.filter(receiver=request.user)

    return render(request, 'messaging/mymessages.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'messages': messages
                  })


@login_required(login_url=reverse_lazy('login'))
def sendmessage(request):
    submitted = False
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            Message = form.save(commit=False)
            try:
                Message.sender = request.user
            except Exception:
                pass
            Message.save()
            return HttpResponseRedirect('/sendmessage?submitted=True')
    else:
        form = MessageForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'messaging/sendmessage.html',
                  {
                      'form': MessageForm,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted
                  })


@login_required(login_url=reverse_lazy('login'))
def message_delete(request, message_id):
    message = Message.objects.get(id=message_id)
    message.delete()
    return render(request,
                  'messaging/message_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })


@login_required(login_url=reverse_lazy('login'))
def message_reply(request, message_id):
    message = Message.objects.get(id=message_id)
    return render(request, 'messaging/message_reply.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'message': message
                  })


def reply(request):
    if request.method == "POST":
        newmessage = Message()
        receiver = request.POST['receiver']
        subject = request.POST['subject']
        message = request.POST['message']

        newmessage.sender = request.user
        newmessage.receiver = User.objects.get(username=receiver)
        newmessage.subject = subject
        newmessage.message = message

        newmessage.save()

        return render(request, 'messaging/message_reply.html', {'message_receiver': newmessage.receiver})
    else:
        return render(request, 'messaging/message_reply.html', {})

