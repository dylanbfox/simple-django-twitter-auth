from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	return HttpResponse("Home")

def welcome(request):
	return HttpResponse("Welcome")

def random(request):
	return HttpResponse("random page..<br /><a href='/twitter/login/'>login</a>")
