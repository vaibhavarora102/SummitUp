from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def simple_upload(request):
    if request.method == 'POST' and request.FILES['vdo']:
        myfile = request.FILES['vdo']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'template/summary.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'template/summary.html')