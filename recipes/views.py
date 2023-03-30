from django.shortcuts import render
from django.http import HttpResponse


def my_view1(request):
    return HttpResponse("HOME")


def my_view2(request):
    return HttpResponse("SOBRE")


def my_view3(request):
    return HttpResponse("CONTATO")
