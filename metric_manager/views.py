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
from django.template import loader
from django.http import HttpResponse
import datetime
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

def delete_note(request):
	if request.method == "POST":
		body = str(request.body.decode('utf-8').replace("\'", "\""))
		body = json.loads(body)
		username = body.get("username")
		text = body.get("text")
		timestamp = body.get("timestamp")
		note_id = body.get("note_id")
		reader_id = FitbitUser.objects.filter(username=username)[0]
		note_row = Notes(id=note_id,id_reader=reader_id,text=text)
		note_row.delete()
		return JsonResponse({'status':1})
	return JsonResponse({'status':0})

def retrieve_notes(request):
	if request.method == "POST":
		body = str(request.body.decode('utf-8').replace("\'", "\""))
		body = json.loads(body)
		username = body.get("username")
		reader_id = FitbitUser.objects.filter(username=username)[0]
		note_list = Notes.objects.filter(id_reader=reader_id).values()
		return JsonResponse({'note_list':list(note_list)})
	return JsonResponse({'status':0})

def retrieve_history_metrics(request):
	if request.method == "POST":
		body = str(request.body.decode('utf-8').replace("\'", "\""))
		body = json.loads(body)
		username = body.get("username")
		type_metric = body.get("type_metric")
		user_id = FitbitUser.objects.filter(username=username)[0]
		id_metric = MetricsDescription.objects.filter(metric_name=type_metric)[0]
		metric_list = Metrics.objects.filter(user_fk=user_id,type=id_metric).values()
		return JsonResponse({'metric_list':list(metric_list)})
	return JsonResponse({'status':1})

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
	weight = body.get('weight');

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
	if weight:
		userRow.weight=weight

	userRow.save()
	return JsonResponse({'status':'1'})

def change_password(request):
	if request.method != 'POST':
		return JsonResponse({'error':'method not permitted'})
	body = str(request.body.decode('utf-8').replace("\'", "\""))
	body = json.loads(body)

	username = body.get('username')
	password_old = body.get('old_password')
	password_new = body.get('password_new')
	password_r = body.get('repeat_password')
	if not username:
		return JsonResponse({'required': 'username'})
	if not password_new:
		return JsonResponse({'required': 'password'})
	if not password_r:
		return JsonResponse({'required': 'repeat_password'})
	if password_new != password_r:
		return JsonResponse({'error': 'password not equal repeat password'})

	user = authenticate(username=username, password=password_old)
	if not user:
		return JsonResponse({'error': 'user not found'})

	user.set_password(password_new)
	user.save()
	return JsonResponse({'status': '1'})


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
	return JsonResponse({'type':metric.type.metric_name,'value':metric.amount})

def insert_metrics(request):
	#check if params are valid
	body = str(request.body.decode('utf-8').replace("\'", "\""))
	body = json.loads(body)
	if request.method!='POST':
		return JsonResponse({'msg':'Wrong method'})
	elif not 'metrics' in body or not 'username' in body:
		return JsonResponse({'msg':'Missing params'})
	username = body['username']
	user_row = FitbitUser.objects.filter(username=username).first()
	for item in json.loads(body['metrics']):
		if MetricsDescription.objects.filter(metric_name=item['metricsDescription']).count()==0:
			continue
		metric_desc = MetricsDescription.objects.filter(metric_name=item['metricsDescription']).first()
		timestamp = datetime.datetime.fromtimestamp(item['timestamp']/1000)
		record = Metrics(user_fk=user_row,amount=item['amount'],type=metric_desc,timestamp=timestamp)
		record.save()
	return JsonResponse({'status':'1'})


class GraphView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self,request):
		if request.GET.get('type')==1:#type param will specify which graph will be returned
			print("type 1")
			template = loader.get_template('livegraph/graph1.html')
		elif request.GET.get('type')==2:
			print("type 2")
			template = loader.get_template('livegraph/graph2.html')
		else:
			template = loader.get_template('livegraph/graph.html')
		context = {}
		return HttpResponse(template.render(context, request))




class AuthView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'Authenticated'}
        return Response(content)
