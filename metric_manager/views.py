from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

# Create your views here.
def index(request):
	return render(request, 'static/index.html')

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('index')
	else:	
		form = UserCreationForm()
	
	context = {'form' : form}
	return render(request, 'registration/register.html', context)

def insert_metrics(request):
	print(request.GET)
	print(request.POST)
	return JsonResponse({'rate':request.POST.get('rate'),
			     'type':request.POST.get('type'),'test':request.GET})
