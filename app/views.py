from django.shortcuts import redirect, render

# Create your views here.
from .forms import ImageForm
from .models import ImageModel


def home(request):
    images = ImageModel.objects.all()
    form = ImageForm()
    if request.method == "POST":
        form = ImageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'images': images, 'form': form}
    return render(request, 'app/home.html', context)
