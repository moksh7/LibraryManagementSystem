from django.shortcuts import redirect, render,HttpResponseRedirect
from django.urls import reverse
from .models import Book,Record
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def homepage(request):
    '''Display all the books'''

    books = Book.objects.all()
    return render(request,'main/home.html',{'books':books})

@login_required
def edit_book(request,id):
    ''' only admin has access to edit books. Select the book object by id passed through URL and change its attributes '''

    if request.user.is_superuser:
        book = Book.objects.get(pk=id)
        if request.method == 'POST':
            bname = request.POST.get('bookname')
            category = request.POST.get('category')
            num = request.POST.get('num')
            book.name = bname
            book.category = category
            book.availability = num
            book.save()
            messages.success(request,'Book Edited successfully')

            return HttpResponseRedirect(reverse('main:home'))

        return render(request,'main/editBook.html',{'book':book})
    else:
        messages.error(request,'Your account doesn\'t have access to this page.')
        return redirect(reverse('main:home'))

@login_required
def add_book(request):
    '''Only the admin has access to add books. Perform checks on data provided and if also book already exists provide a link to edit book    '''

    if request.user.is_superuser:
        if request.method=='POST':
            bname = request.POST.get('bookname')
            category = request.POST.get('category')
            num = request.POST.get('num')
            bookobj = Book.objects.filter(name=bname,category=category)
            if bookobj:
                messages.info(request,'book already exists')
                return render(request,'main/addBook.html',{'book':bookobj[0]})
            elif len(bname) <2:
                messages.error(request,'book name too short')
            elif len(category) <2:
                messages.error(request,'category too short')
            else:
                Book.objects.create(name=bname,category=category,availability=num)
                messages.success(request,'Book Added!')
                return HttpResponseRedirect(reverse('main:home'))
        return render(request,'main/addBook.html')
    else:
        messages.error(request,'Your account doesn\'t have access to this page.')
        return redirect(reverse('main:home'))

@login_required
def delete(request,id):
    '''only admin has access to delete books. Select the book object by id passed through URL and delete the object'''
    
    if request.user.is_superuser:
        book = Book.objects.get(pk=id)
        book.delete()
        messages.error(request, 'Book deleted')
    else:
        messages.error(request,'Your account doesn\'t have access to this page.')
    return redirect(reverse('main:home'))

@login_required
def issue_book(request,id):
    '''Select the student through request object, Select the book object by id passed through URL. Check if student has already issued this book, availability of the book, and enforce student can only issued 3 books. Add the book to Student m2m relation with the Book'''

    student = request.user.student
    book = Book.objects.get(pk=id)
    if book in student.books_issued.all():
        messages.error(request,'you already have issued this book')
        return redirect(reverse('main:booksissued'))
    elif book.availability <1:
        messages.error(request,'No books available')
        return redirect(reverse('main:home'))

    elif not (student.books_issued.all().count() <3):
        messages.error(request,'you already have issued 3 books return a book to issue a new one')
        return redirect(reverse('main:booksissued'))
    else:
        student.books_issued.add(book)
        book.availability -= 1
        book.save()
        return HttpResponseRedirect(reverse('main:booksissued'))

@login_required
def display_all_issued_books(request):
    '''only admin has access to view all issued books.'''
    if request.user.is_superuser:
        records = Record.objects.all()
        return render(request,'main/allIssuedBooks.html',{'records':records})
    else:
        messages.error(request,'Your account doesn\'t have access to this page.')
        return redirect(reverse('main:home'))

@login_required
def returnbook(request,id):
    '''Select the student through request object, Select the book object by id passed through URL.Remove the book from Student m2m relation with the Book'''
    student = request.user.student
    book = Book.objects.get(pk=id)
    if book in student.books_issued.all():
        student.books_issued.remove(book)
        book.availability +=1
        book.save()
        return HttpResponseRedirect(reverse('main:home'))
    else:
        messages.error(request,'you have not issued this book')
        return HttpResponseRedirect(reverse('main:home'))

@login_required
def books_issued(request):
    ''' list all books issued by a student'''
    student = request.user.student
    records = student.record_set.all()
    return render(request,'main/books.html',{'records':records})