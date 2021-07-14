from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('matzip_image/index.html')
    return HttpResponse(template.render(request))

# def image_show(request, file_name):
#
