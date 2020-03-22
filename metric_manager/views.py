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
from pytz import timezone
from datetime import date
import pytz
from django.db.models import Avg
from django.db.models import Sum
from datetime import timedelta
import datetime
from datetime import date, timedelta
from django.db.models import F
# Create your views here.


def index(request):
	return render(request, 'static/index.html')


class Register(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		if request.method == 'POST':
			form = MyRegistrationForm(request.POST)
			if form.is_valid():
				form.save()
				username = form.cleaned_data['username']
				password = form.cleaned_data['password1']
				is_specialist = form.cleaned_data['type']
				user = authenticate(username=username, password=password,is_specialist=is_specialist)
				login(request, user)
				return redirect('index')
		else:
			form = MyRegistrationForm()

		context = {'form' : form}
		return render(request, 'registration/register.html', context)


class SaveNotes(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		if request.method == "POST":
			body = str(request.body.decode('utf-8').replace("\'", "\""))
			body = json.loads(body)
			owner = body.get('owner')
			reader = body.get('reader')
			description = body.get('description')
			# note = (owner,reader,description)
			writer_id = FitbitUser.objects.filter(username=owner)[0]
			reader_id = FitbitUser.objects.filter(username=reader)[0]
			note_row = Notes(id_writer=writer_id,id_reader=reader_id,text=description)
			note_row.save()
			return JsonResponse({'status':1})
		return JsonResponse({'status':0})

class DeleteNotes(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
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

class RetrieveUsers(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		if request.method == "POST":
			body = str(request.body.decode('utf-8').replace("\'", "\""))
			body = json.loads(body)
			username = body.get("username")
			specialist_id = FitbitUser.objects.filter(username=username)[0]
			temp_list = Monitor.objects.filter(from_user=specialist_id).values()
			patient_list = []
			for temp in temp_list:
				user_info = FitbitUser.objects.filter(id=temp['to_user_id'])[0]
				patient_user = user_info.username
				patient_birth = user_info.birthdate
				patient_joined = user_info.date_joined
				patient_list.append({'username':patient_user,'birthdate':patient_birth,'date_joined':patient_joined})
			return JsonResponse({'patient_list':patient_list})
		return JsonResponse({'status':0})


class RetrieveNotes(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		if request.method == "POST":
			body = str(request.body.decode('utf-8').replace("\'", "\""))
			body = json.loads(body)
			username = body.get("username")
			reader_id = FitbitUser.objects.filter(username=username)[0]
			note_list = Notes.objects.filter(id_reader=reader_id).values()
			specialist_list = []
			patient_list = []
			for i in range(len(note_list)):
				if (note_list[i]['id_writer_id']==note_list[0]['id_reader_id']):
					patient_list.append(note_list[i])
				else:
					specialist_list.append(note_list[i])
			return JsonResponse({'patient_list':patient_list,'specialist_list':specialist_list})
		return JsonResponse({'status':0})

# class IsSpecialist(APIView):
# 	permission_classes = (IsAuthenticated,)
# 	def post(self,request):
# 		if request.method == "POST":
# 			import pdb; pdb.set_trace()
# 			body = str(request.body.decode('utf-8').replace("\'", "\""))
# 			body = json.loads(body)
# 			username = body.get("username")
# 			get_details = FitbitUser.objects.filter(username=username)

def is_specialist(request):
	if request.method == "POST":
		body = str(request.body.decode('utf-8').replace("\'", "\""))
		body = json.loads(body)
		username = body.get("username")
		get_details = FitbitUser.objects.filter(username=username).values()[0]
		return JsonResponse({'is_specialist':get_details['is_specialist']})
	return JsonResponse({'status':-1})

class RetrieveHistoryMetrics(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		if request.method == "POST":
			try:
				body = str(request.body.decode('utf-8').replace("\'", "\""))
				body = json.loads(body)
				username = body.get("username")
				type_metric = body.get("type_metric")
				startDate = body.get("startDate")
				endDate = body.get("endDate")
			except Exception as e:
				username=request.POST['username']
				type_metric=request.POST['type_metric']
				startDate=request.POST['startDate']
				endDate=request.POST['endDate']
			start_list = startDate.split("-")
			end_list = endDate.split("-")

			sdate = date(int(start_list[0]), int(start_list[1]), int(start_list[2]))   # start date
			edate = date(int(end_list[0]), int(end_list[1]), int(end_list[2]))   # end date

			delta = edate - sdate       # as timedelta
			dates_list = []
			for i in range(delta.days + 1):
				day = sdate + timedelta(days=i)
				dates_list.append(day)

			user_id = FitbitUser.objects.filter(username=username)[0]
			id_metric = MetricsDescription.objects.filter(metric_name=type_metric)[0]
			final_list = []
			metric_list = Metrics.objects.filter(user_fk=user_id,type=id_metric).values()
			for i in range(len(metric_list)):
				current_date = metric_list[i]["timestamp"]
				if ((current_date.year>=int(start_list[0]) and current_date.year<=int(end_list[0])) and
					(current_date.month>=int(start_list[1]) and current_date.month<=int(end_list[1])) and
					(current_date.day>int(start_list[2]) and current_date.day<=int(end_list[2]))):
					final_list.append(metric_list[i])
			return JsonResponse({'metric_list':final_list,'dates_list':dates_list})
		return JsonResponse({'status':1})

def retrieve_history_metrics(request):
	if request.method == "POST":
		body = str(request.body.decode('utf-8').replace("\'", "\""))
		body = json.loads(body)
		username = body.get("username")
		type_metric = body.get("type_metric")
		startDate = body.get("startDate")
		endDate = body.get("endDate")
		start_list = startDate.split("-")
		end_list = endDate.split("-")

		sdate = date(int(start_list[0]), int(start_list[1]), int(start_list[2]))   # start date
		edate = date(int(end_list[0]), int(end_list[1]), int(end_list[2]))   # end date

		delta = edate - sdate       # as timedelta
		dates_list = []
		for i in range(delta.days + 1):
		    day = sdate + timedelta(days=i)
		    dates_list.append(day)

		user_id = FitbitUser.objects.filter(username=username)[0]
		id_metric = MetricsDescription.objects.filter(metric_name=type_metric)[0]
		final_list = []
		metric_list = Metrics.objects.filter(user_fk=user_id,type=id_metric).values()
		for i in range(len(metric_list)):
			current_date = metric_list[i]["timestamp"]
			if ((current_date.year>=int(start_list[0]) and current_date.year<=int(end_list[0])) and
				(current_date.month>=int(start_list[1]) and current_date.month<=int(end_list[1])) and
				(current_date.day>int(start_list[2]) and current_date.day<=int(end_list[2]))):
				final_list.append(metric_list[i])
		return JsonResponse({'metric_list':final_list,'dates_list':dates_list})
	return JsonResponse({'status':1})

def register_api(request):
	body = str(request.body.decode('utf-8').replace("\'", "\""))
	body = json.loads(body)
	username = body.get('username')
	password = body.get('password')
	password_r = body.get('repeat_password')
	if body.get('type') == 'specialist_select':
		type=True
	else:
		type=False

	if not username:
		return JsonResponse({'required':'username'})
	if not password:
		return JsonResponse({'required':'password'})
	if not password_r:
		return JsonResponse({'required':'repeat_password'})
	if not body.get('type'):
		return JsonResponse({'required':'type'})
	if password!=password_r:
		return JsonResponse({'error':'password not equal repeat password'})
	if len(FitbitUser.objects.filter(username=username))>0:
		return JsonResponse({'error':'username already exists'})
	user = FitbitUser.objects.create_user(username,'testmail@test.com',password,is_specialist=type)
	login(request,user)
	return JsonResponse({'status':1})

class EditProfileApi(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		if request.method != 'POST':
			return JsonResponse({'error':'method not permitted'})
		body = str(request.body.decode('utf-8').replace("\'", "\""))
		body = json.loads(body)
		username = body.get('username')
		if not username:
			return JsonResponse({'error':'username missing'})

		userRow = FitbitUser.objects.filter(username=request.user).first()
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

class GetUserInfo(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self,request):
		res_dict = json.loads(serializers.serialize('json', [request.user]))[0]['fields']
		res_dict.pop('password')
		return JsonResponse(res_dict,safe=False)


def fill_missing_values(start_date,end_date,metric):
	result = []
	currDate = start_date.date()
	curr_idx = 0
	while(currDate<=end_date.date()):
		if curr_idx<len(metric) and metric[curr_idx]['day']==currDate:
			result.append(metric[curr_idx])
			curr_idx+=1
		else:
			result.append({'day':currDate,'amount':0})
		currDate+=timedelta(days=1)
	return result

class GetSpecialist(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self,request):
		if request.method=='GET':
			specialist_list =  FitbitUser.objects.filter(is_specialist=True).values('username',
																				'first_name',
																				'last_name',
																				'email',
																				'telephone',
																				'address',
																				'gender',
																				'birthdate')
		if not specialist_list:
			return JsonResponse({'msg':'No specialist in database'})
		return JsonResponse({'docs':list(specialist_list)})


class AllMetricsView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self,request):
		if len(request.GET)==0 or not 'from' in request.GET or not 'username' in request.GET or not 'to' in request.GET:
			return JsonResponse({'msg':'invalid request'})

		fromDate = request.GET.get('from')
		toDate = request.GET.get('to')
		local_timezone = timezone('Europe/Athens')
		fromDate = datetime.datetime.strptime(fromDate,'%Y-%m-%d').astimezone(local_timezone)
		toDate =datetime.datetime.strptime(toDate,'%Y-%m-%d').astimezone(local_timezone)
		user = request.GET.get('username')
		user_id = FitbitUser.objects.filter(username=user)[0]
		user_metrics = Metrics.objects.filter(user_fk=user_id , timestamp__range=(fromDate,toDate)) \
									  .values('timestamp','amount','type')
		heart=Metrics.objects.filter(type=1, timestamp__range=(fromDate,toDate)) \
							 .extra(select={'day': 'date(timestamp)'}) \
							 .values('day') \
							 .annotate(amount=Avg('amount')) \
							 .order_by('day')

		calories= Metrics.objects.filter(type=2, timestamp__range=(fromDate,toDate)) \
								 .extra(select={'day': 'date(timestamp)'}) \
								 .values('day') \
								 .annotate(amount=Sum('amount')) \
								 .order_by('day') \

		distance= Metrics.objects.filter(type=3, timestamp__range=(fromDate,toDate)) \
								 .extra(select={'day': 'date(timestamp)'}) \
								 .values('day') \
								 .annotate(amount=Sum('amount')) \
								 .order_by('day')
		heart = fill_missing_values(fromDate,toDate,heart)
		calories = fill_missing_values(fromDate,toDate,calories)
		distance = fill_missing_values(fromDate,toDate,distance)
		if len(user_metrics)==0:
			return JsonResponse({'type':request.GET.get('type'),'value':0})
		#return JsonResponse({'metrics': list(user_metrics)})
		return JsonResponse({'heart':list(heart), 'calories': list(calories), 'distance': list(distance) })

class LatestValueView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self,request):
		if len(request.GET)==0 or not 'type' in request.GET:
			return JsonResponse({'msg':'invalid request'})
		metric_desc = MetricsDescription.objects.filter(metric_name=request.GET.get('type'))
		user_row = request.user#change with user name
		if not user_row:
			return JsonResponse({'msg':'missing user'})
		if not metric_desc:
			return JsonResponse({'msg':'Wrong type'})
		metric = Metrics.objects.filter(type=metric_desc[0])
		if len(metric)==0:
			return JsonResponse({'type':request.GET.get('type'),'value':0})
		metric = metric.latest('timestamp')
		return JsonResponse({'type':metric.type.metric_name,'value':metric.amount})

'''
This endpoint will allow specialist to monitor any user
'''
class UserLatestMetric(APIView):
	permission_classes = (IsAuthenticated,)
	'''
	params:
	username:The user that the specialist has access to monitor
	'''
	def get(self,request):
		if not request.GET.get('username') or not request.GET.get('type'):
			return JsonResponse({'status':0,'msg':'missing fields'})
		username = request.GET.get('username')
		type = request.GET.get('type')
		user_row = FitbitUser.objects.filter(username=username).first()
		metric_desc = MetricsDescription.objects.filter(metric_name=request.GET.get('type'))
		if not user_row:
			return JsonResponse({'status':0,'msg':'user not found'})
		request_row = Monitor.objects.filter(from_user=user_row,to_user=request.user,completed=True).first()
		if not user_row and request.user.username!=username:
			return JsonResponse({'status':0,'msg':'no granted access'})
		metric = Metrics.objects.filter(user_fk=user_row,type=metric_desc[0])
		if len(metric)==0:
			return JsonResponse({'type':request.GET.get('type'),'value':0})
		metric = metric.latest('timestamp')
		return JsonResponse({'type':metric.type.metric_name,'value':metric.amount})


def insert_metrics(request):
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
		local_timezone = timezone('Europe/Athens')
		timestamp = datetime.datetime.fromtimestamp(item['timestamp']/1000).astimezone(local_timezone)
		# import pdb;pdb.set_trace()
		# timestamp+=datetime.timedelta(hours=2)
		record = Metrics(user_fk=user_row,amount=item['amount'],type=metric_desc,timestamp=timestamp)
		record.save()
	return JsonResponse({'status':'1'})


class GraphView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self,request):
		token = request.META.get('HTTP_AUTHORIZATION')
		if request.GET.get('type')=='1':#type param will specify which graph will be returned
			context = {'token':token}
			template = loader.get_template('livegraph/graph1.html')
		elif request.GET.get('type')=='2':
			# import pdb;pdb.set_trace()
			start_date = request.GET.get('start_date')
			end_date = request.GET.get('end_date')
			context = {'token':token,
					   'start_date':start_date,
					   'end_date':end_date,
					   'username':request.user.username}
			template = loader.get_template('historygraph/calories.html')
		elif request.GET.get('type')=='3':
			# import pdb;pdb.set_trace()
			start_date = request.GET.get('start_date')
			end_date = request.GET.get('end_date')
			context = {'token':token,
					   'start_date':start_date,
					   'end_date':end_date,
					   'username':request.user.username}
			template = loader.get_template('historygraph/heart.html')
		else:
			context = {'token':token}
			template = loader.get_template('livegraph/graph.html')
		return HttpResponse(template.render(context, request))




class AuthView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        content = {'message': 'Authenticated'}
        return Response(content)


class PermissionManager(APIView):
	permission_classes = (IsAuthenticated,)
	'''
	POST params:
	if patient:
		username:The specialist who will receive the permission request
	if specialist:
		username:The user who will be accepted to be monitored
	'''
	def post(self,request):
		print(request.user.username)
		body = str(request.body.decode('utf-8').replace("\'", "\""))
		body = json.loads(body)

		username = body['username']
		if not username:
			return JsonResponse({'status':0,'msg':'missing fields'})
		if len(FitbitUser.objects.filter(username=username))==0:
			return JsonResponse({'status':0,'msg':'user not found'})
		if(
			request.user.is_specialist
			and not FitbitUser.objects.filter(username=username).first().is_specialist
		):
			if body.get('reject') and body['reject']==True:
				rejected=True
			else:
				rejected=False
			from_user = FitbitUser.objects.filter(username=username).first()
			to_user = request.user
			req = Monitor.objects.filter(from_user=from_user,to_user=to_user).first()
			if rejected:
				user_deleted = req.from_user
				response_user = {'username':user_deleted.username,
								 'first_name':user_deleted.first_name,
								 'last_name':user_deleted.last_name,
								 'telephone':user_deleted.telephone}
				user = req.delete()
				print(response_user)
				return JsonResponse({'status':1,
									 'msg':'Rejected successfuly',
									 'user':list(response_user)})
			req.completed=True
			req.save()
		elif(
			not request.user.is_specialist
			and FitbitUser.objects.filter(username=username).first().is_specialist
		):
			if body.get('reject') and body['reject']==True:
				rejected=True
			else:
				rejected=False
			from_user = request.user
			to_user = FitbitUser.objects.filter(username=username).first()
			#store in db that request is sent
			if len(Monitor.objects.filter(from_user=request.user,to_user=to_user,completed=False))==0:
				permission_record = Monitor(from_user=request.user,to_user=to_user)
				permission_record.save()
			elif rejected:
				user_row = Monitor.objects.filter(from_user=request.user,to_user=to_user)
				user_deleted = user_row.first().to_user
				response_user = {'username':user_deleted.username,
								 'first_name':user_deleted.first_name,
								 'last_name':user_deleted.last_name,
								 'telephone':user_deleted.telephone}
				user_row.delete()
				return JsonResponse({'status':1,
									 'msg':'Rejected successfuly',
									 'user':list(response_user)})
		else:
			return JsonResponse({'status':0,'msg':'Wrong user type'})
			#update db that request has been accepted

		return JsonResponse({'status':1})

	'''
	if specialist : returns all requests from users received and if accepted
	if patient:returns all requests sent and if accepted
	'''
	def get(self,request):
		if request.user.is_specialist:
			users = Monitor.objects.filter(to_user=request.user) \
								   .annotate(username=F('from_user__username')) \
								   .annotate(first_name=F('from_user__first_name')) \
								   .annotate(last_name=F('from_user__last_name')) \
								   .annotate(telephone=F('from_user__telephone')) \
								   .values('username','first_name','last_name','telephone','completed')
			return JsonResponse({'users':list(users)})

		specialists_sent = Monitor.objects.filter(from_user=request.user) \
	  								      .annotate(username=F('to_user__username')) \
	  								      .annotate(first_name=F('to_user__first_name')) \
	  								      .annotate(last_name=F('to_user__last_name')) \
	  								      .annotate(telephone=F('to_user__telephone')) \
								   		  .values('username','first_name','last_name','telephone','completed')
		excluded_specialists = Monitor.objects.filter(from_user=request.user) \
											  .values_list('to_user__id',flat=True)
		specialists_not_sent = FitbitUser.objects.filter(is_specialist=True) \
												 .exclude(id__in=excluded_specialists) \
												 .exclude(username=request.user.username) \
												 .values('username','first_name','last_name','telephone')
		return JsonResponse({'specialists_sent':list(specialists_sent),
							 'specialists_not_sent':list(specialists_not_sent)})
