from django.shortcuts import render, redirect
from .models import GalleryImage, SliderImage
from .forms import GalleryImageForm

def galery(request):
    slider = SliderImage.objects.filter(active=True).order_by('order')
    return render(request, 'gallery/index.html', {"slider_images": slider})

def upload(request):
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    form = GalleryImageForm()
    return render(request, 'gallery/upload.html', {"form": form})
