from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login , logout
from django.http import JsonResponse
import sys
from .models import *
from .forms import *
import json
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt
def save_note(request):
	# import pdb;pdb.set_trace()
	if request.method == "POST":
		body = str(request.body.decode('utf-8').replace("\'", "\""))
		body = json.loads(body)
		owner = body.get('owner')
		reader = body.get('reader')
		description = body.get('description')
		# note = (owner,reader,description)
		writer_id = FitbitUser.objects.filter(username=reader)[0]
		note_row = Notes(id_writer=writer_id,id_reader=writer_id,text=description)
		note_row.save()
		return JsonResponse({'status':1})
	return JsonResponse({'status':0})

def register_api(request):
	body = str(request.body.decode('utf-8').replace("\'", "\""))
	body = json.loads(body)
	username = body.get('username')
	password = body.get('password')
	password_r = body.get('repeat_password')
	if not username:
		return JsonResponse({'required':'username'})
	if not password:
		return JsonResponse({'required':'password'})
	if not password_r:
		return JsonResponse({'required':'repeat_password'})
	if password!=password_r:
		return JsonResponse({'error':'password not equal repeat password'})
	if len(FitbitUser.objects.filter(username=username))>0:
		return JsonResponse({'error':'username already exists'})
	user = FitbitUser.objects.create_user(username,'testmail@test.com',password)
	login(request,user)
	return JsonResponse({'status':1})

def edit_profile_api(request):
	if request.method != 'POST':
		return JsonResponse({'error':'method not permitted'})
	body = str(request.body.decode('utf-8').replace("\'", "\""))
	body = json.loads(body)

	username = body.get('username')
	if not username:
		return JsonResponse({'error':'username missing'})

	userRow = FitbitUser.objects.filter(username=username).first()
	if not userRow:
		return JsonResponse({'error':'user not found'})

	name = body.get('name')
	surname = body.get('surname')
	birthday = body.get('birthday')
	height = body.get('height')
	gender = body.get('gender')
	email = body.get('email')
	password = body.get('password')
	telephone = body.get('telephone')
	address = body.get('address')

	if name:
		userRow.first_name=name
	if surname:
		userRow.last_name=surname
	if birthday:
		userRow.birthdate=birthday
	if height:
		userRow.height=height
	if gender:
		userRow.gender=gender
	if email:
		userRow.email=email
	if password:
		userRow.set_password(password)
	if telephone:
		userRow.telephone=telephone
	if address:
		userRow.address=address

	userRow.save()
	return JsonResponse({'status':'1'})

def login_api(request):
	if request.method == "POST":
		body = str(request.body.decode('utf-8').replace("\'", "\""))
		body = json.loads(body)
		username = body.get('username')
		password = body.get('password')
		if username is None or password is None:
			return JsonResponse({'required_fields':'username , password'})
		sys.stderr.write(username+" "+password)
		user = authenticate(username=username, password=password)
		if user:
			return JsonResponse({'status':1})
	return JsonResponse({'status':0})

def logout_api(request):
	logout(request)
	return JsonResponse({'status':1})

def get_user_info(request):
	if request.method=='POST':
		body = str(request.body.decode('utf-8').replace("\'", "\""))
		body = json.loads(body)
		username = body.get('username')
		if not username:
			return JsonResponse({'error':'missing username'})
		userRow = FitbitUser.objects.filter(username=username)
		if not userRow:
			return JsonResponse({'error':'user does not exist'})
		res_dict = json.loads(serializers.serialize('json', userRow))[0]['fields']
		res_dict.pop('password')
		return JsonResponse(res_dict,safe=False)

def get_latest_value(request):
	sys.stderr.write(str(request.GET.get('type')))
	if len(request.GET)==0 or not 'type' in request.GET:
		return JsonResponse({'msg':'invalid request'})
	metric_desc = MetricsDescription.objects.filter(metric_name=request.GET.get('type'))
	user_row = FitbitUser.objects.first()#change with user name
	if not user_row:
		return JsonResponse({'msg':'missing user'})
	if not metric_desc:
		return JsonResponse({'msg':'Wrong type'})
	metric = Metrics.objects.filter(type=metric_desc[0])
	if len(metric)==0:
		return JsonResponse({'type':request.GET.get('type'),'value':0})
	metric = metric.latest('timestamp')
	return JsonResponse({'type':metric.type,'value':metric.amount})

def insert_metrics(request):
	#check if params are valid
	if len(request.GET)>0 and 'type' in request.GET and 'value' in request.GET:
		metric_desc = MetricsDescription.objects.filter(metric_name=request.GET.get('type'))
		if not metric_desc:
			return JsonResponse({'msg':'Wrong type'})
		metric = Metrics(type=metric_desc[0],amount=request.GET.get('value'))
		metric.save()
	return JsonResponse({'test':request.GET})

def live_graph(request):
	return render(request,'livegraph/graph.html')

def get_token(request):
	pass


class AuthView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Authenticated'}
        return Response(content)
