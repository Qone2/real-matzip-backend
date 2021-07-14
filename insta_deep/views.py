from django.shortcuts import render
from django.http import HttpResponse
import sys
import insta

driver = insta.open_driver()


def index(request):
    return HttpResponse("Hello, world. You're at the insta_deep index.")


def insta_activate(request, keyword):
    insta.matzip_deep(driver, keyword)
    return HttpResponse("%s으로 크롤링 완료" % keyword)
