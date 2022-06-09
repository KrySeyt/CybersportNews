from django.http import HttpRequest
from django.shortcuts import render, HttpResponse


def main(request: HttpRequest):
    return HttpResponse("Work in progress")
