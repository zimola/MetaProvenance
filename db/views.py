from django.shortcuts import render


def search(request):
    return render(request, 'db/search.html', context={})


def browse(request):
    return render(request, 'db/browse.html', context={})


def upload(request):
    return render(request, 'db/upload.html', context={})
