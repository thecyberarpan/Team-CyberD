from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.


def Index(request):
    return render(request, 'mainapp/index.html')


def About(request):
    return render(request, 'mainapp/about.html')


def Blog(request):
    blogs = Blogpost.objects.all().order_by('-id')
    params = {'blogs': blogs}
    return render(request, 'mainapp/Blog.html', params)


def BlogDetails(request, slug):
    blog = Blogpost.objects.get(slug = slug)
    params = {'blog': blog}
    return render(request, 'mainapp/blog-details.html', params)


def Contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        messages.success(request, "Your message have been submitted successfully")
        return redirect('Contact')
    return render(request, 'mainapp/Contact.html')
