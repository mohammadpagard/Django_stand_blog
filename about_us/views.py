from django.shortcuts import render



def about(request):
    return render(request, 'about_us/about.html', {})