from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
import datetime
from .forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class BookListView(generic.ListView):
    model = Book
    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(BookListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['some_data'] = 'This is just some data'
        return context
class BookDetailView(generic.DetailView):
    model = Book

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


def index(request):
    """View function for home page of site."""

    # Получаем количество основных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.all().count()

    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # Количество жанров
    num_genres = Genre.objects.all().count()

    # Количество книг, содержащих определенное слово в заголовке (без учета регистра)
    search_word = request.GET.get('search', 'How')
    num_books_with_word = Book.objects.filter(
        Q(title__icontains=search_word) | Q(summary__icontains=search_word)
    ).count()

    # Количество посещений этой view, подсчитанное в переменной session
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_with_word': num_books_with_word,
        'search_word': search_word,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10  # Пагинация по 10 авторов на странице
    template_name = 'catalog/author_list.html'
    context_object_name = 'author_list'

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'

class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/all_borrowed_books.html'
    paginate_by = 10

    def get_queryset(self):
        # Получаем только взятые книги (статус 'o' - on loan)
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()
            return redirect('all-borrowed')
    else:
        form = RenewBookForm()

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'book_instance': book_instance})
class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre']
    permission_required = 'catalog.add_book'
    template_name = 'catalog/book_form.html'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre']
    permission_required = 'catalog.change_book'
    template_name = 'catalog/book_form.html'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.delete_book'
    template_name = 'catalog/book_confirm_delete.html'