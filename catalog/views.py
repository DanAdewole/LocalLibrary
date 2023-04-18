import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.db.models import Q

from .models import Book, Author, BookInstance, Genre, Language
from catalog.forms import RenewBookForm, CreateBookInstanceForm, CustomPasswordResetForm, CustomUserCreationForm


# def index(request):
#     """View function for home page of site."""

#     # Generate counts of some of the main objects
#     num_books = Book.objects.all().count()
#     num_instances = BookInstance.objects.all().count()

#     # Available books (status = 'a')
#     num_instances_available = BookInstance.objects.filter(status__exact="a").count()

#     # The all() is implied by default.
#     num_authors = Author.objects.count()

#     # Counts for genres and books containing "fiction"
#     num_genres_fiction = Genre.objects.filter(name__icontains="fiction").count()
#     num_books_fiction = Book.objects.filter(title__icontains="fiction").count()

#     # Number of visits to this view, as counted in the session variable.
#     num_visits = request.session.get("num_visits", 0)
#     request.session["num_visits"] = num_visits + 1

#     context = {
#         "num_books": num_books,
#         "num_instances": num_instances,
#         "num_instances_available": num_instances_available,
#         "num_authors": num_authors,
#         "num_genres_fiction": num_genres_fiction,
#         "num_books_fiction": num_books_fiction,
#         "num_visits": num_visits,
#     }

#     # Render the HTML template index.html with the data in the context variable
#     return render(request, "index.html", context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "index.html"
    paginate_by = 5

    def get_queryset(self):
        # return Book.objects.filter(title__icontains="fiction")[:5]
        return Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context["all_genre"] = Genre.objects.all()
        return context


class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = "book_detail.html"


class BookInstanceCreateView(LoginRequiredMixin, CreateView):
    model = BookInstance
    form_class = CreateBookInstanceForm
    # fields = ['imprint', 'due_back', 'status']
    # context_object_name = "bookinstance"
    template_name = 'bookinstance_form.html'
    success_url = reverse_lazy('my-borrowed')
    
    def form_valid(self, form):
        form.instance.borrower = self.request.user
        form.instance.book = get_object_or_404(Book, id=self.kwargs['book_id'])
        form.instance.status = 'o'
        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        initial['status'] = 'o'  # Set status to "On loan"
        initial['borrower'] = self.request.user  # Set borrower to current user
        initial['book'] = get_object_or_404(Book, id=self.kwargs['book_id'])  # Set book to clicked book
        return initial
    
    def get_context_data(self, **kwargs):
        context = super(BookInstanceCreateView, self).get_context_data(**kwargs)
        context["book"] = Book.objects.get(pk=self.kwargs['book_id'])
        return context


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = "author_list"
    template_name = "author_list.html"
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author
    context_object_name = "author"
    template_name = "author_detail.html"
    paginate_by = 10


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    model = BookInstance
    template_name = "bookinstance_list.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )


class LoanedBooksAllListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan."""

    model = BookInstance
    template_name = "bookinstance_list_all.html"
    context_object_name = "bookinstance_list_all"
    paginate_by = 10
    permission_required = ("catalog.can_mark_returned")

    def get_queryset(self):
        return (BookInstance.objects.filter(status__exact="o").order_by("due_back"))


# Get all books with a particular genre
class BookGenreListview(generic.ListView):
    template_name = "book_list_by_genre.html"
    context_object_name = "books"
    paginate_by = 10
    
    def get_queryset(self):
        genre = self.kwargs["genre"]
        queryset  = Book.objects.filter(genre__name__in=[genre])
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(BookGenreListview, self).get_context_data(**kwargs)
        context["genre"] = self.kwargs["genre"]
        context["all_genre"] = Genre.objects.all()
        return context

# as a function based view
# def book_detail_view(request, primary_key):
#     try:
#         book = Book.objects.get(pk=primary_key)
#     except Book.DoesNotExist:
#         raise Http404('Book does not exist')

#     return render(request, 'catalog/book_detail.html', context={'book': book})


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'book_renew_librarian.html', context)


class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '05/01/2023'}
    permission_required = ('catalog.add_author')
    template_name = 'author_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creating'] = True
        return context
    

class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__'  # Not recommended (potential security issue if more fields added)
    permission_required = ('catalog.change_author')
    template_name = 'author_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creating'] = False
        return context
    
    
class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = ('catalog.delete_author')
    template_name = "author_confirm_delete.html"


class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = ('catalog.add_book')
    template_name = "book_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creating'] = True
        return context
    

class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'  # Not recommended (potential security issue if more fields added)
    permission_required = ('catalog.change_book')
    template_name = "book_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creating'] = False
        return context
    

class BookDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('index')
    permission_required = ('catalog.delete_book')
    template_name = "book_confirm_delete.html"
    

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'password_reset.html'


def signup(request):
    if request.method == 'POST':
        form  = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password = password)
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
    
    
class SearchResultsView(generic.ListView):
    model = Book
    template_name = 'book_search.html'
    context_object_name = 'book_search'
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            # Search for books that match the query in title or author's name
            return Book.objects.filter(
                Q(title__icontains=query) | Q(author__first_name__icontains=query) | Q(summary__icontains=query) | Q(author__last_name__icontains=query)
                # Q(title__icontains=query) | Q(summary__icontains=query)
            )
        else:
            return Book.objects.none()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q")
        context["search_term"] = query
        return context


def about_me_view(request):
    return render(request, "about_me.html")


def about_project_view(request):
    return render(request, "about_project.html")
