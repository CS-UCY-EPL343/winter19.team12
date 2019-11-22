from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import sys
from .models import *
from .forms import *

# Create your views here.
def index(request):
	return render(request, 'static/index.html')

def register(request):
	if request.method == 'POST':
		form = MyRegistrationForm(request.POST)

		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('index')
	else:
		form = MyRegistrationForm()

	context = {'form' : form}
	return render(request, 'registration/register.html', context)

def get_latest_value(request):
	sys.stderr.write(str(request.GET.get('type')))
	if len(request.GET)==0 or not 'type' in request.GET:
		return JsonResponse({'msg':'invalid request'})
	metric = Metrics.objects.filter(type=request.GET.get('type')).latest('timestamp')
	return JsonResponse({'type':metric.type,'value':metric.amount})

def insert_metrics(request):
	sys.stderr.write("lenntff:"+str(len(request.GET)))
	sys.stderr.write(str(request.GET.get('value')))
	#check if params are valid
	if len(request.GET)>0 and 'type' in request.GET and 'value' in request.GET:
		sys.stderr.write("testt")
		sys.stderr.write('valid request')
		metric = Metrics(type=request.GET.get('type'),amount=request.GET.get('value'))
		metric.save()
	return JsonResponse({'test':request.GET})

def live_graph(request):
	return render(request,'livegraph/graph.html')
