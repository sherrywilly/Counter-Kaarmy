from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json
from django.db.models import Q
from counter.models import *
from django.db.utils import IntegrityError
from uuid import uuid4

# Create your views here.
User = get_user_model()

# ! get the user by username or email or id for search


def get_user_by_name(request, name):
    try:
        m = int(name)
    except:
        m = None
    x = User.objects.filter(Q(username__contains=name) | Q(
        email__icontains=name) | Q(id=m))
    l = []

    for i in x:
        y = dict()
        y = {
            'username': i.username,
            'id': i.pk
        }
        l.append(y)

    return JsonResponse({'data': l})

#! get employeee data for the update


def get_employee_data(request, id):
    try:
        _x = Employee.objects.get(id=id)

        context = {
            'error': 'false',
            'data': {
                'id': _x.pk,
                'username': _x.user.username,
                'empid': _x.user.pk,
                'position': _x.position,
                'status': _x.status,
                'join_date': _x.j_date

            }
        }
        # ? if user id does not exist may couse error
    except:
        context = {
            'error': 'true',
            'message': 'invalid user id'
        }
    return JsonResponse(context)

# !create and update for Employee model


@csrf_exempt
def create_or_update_employee(request):
    if request.method == 'POST':
        uname = request.POST.get('username')

        c = Employee.objects.filter(
            user__username=uname, status__in=['0', '1'])
        if c:
            return JsonResponse({'error': 'true', 'message': 'this Employee is working on an'})
        eid = request.POST.get('eid')
        pos = request.POST.get('position')
        jdate = request.POST.get('join_date')
        status = request.POST.get('status')
        try:
            x, m = Employee.objects.get_or_create(
                user_id=eid, emp_id=eid, position=pos, j_date=jdate)
            if not m:
                raise ValueError
            context = {
                'error': 'false',
                'data': {
                    'username': x.user.username,
                    'empid': x.user.pk,
                    'position': x.position,
                    'status': x.status,
                    'join_date': x.j_date

                },
                'message': 'employee created successfully'

            }
            # ? if update request may cause Integrity error
        except:
            x = Employee.objects.get(user_id=eid)
            x.position = pos
            x.j_date = jdate
            x.status = status
            x.save()
            context = {
                'error': 'false',
                'data': {
                    'username': x.user.username,
                    'empid': x.user.pk,
                    'position': x.position,
                    'status': x.status,
                    'join_date': x.j_date

                },
                'message': 'employee updated successfully'

            }
        return JsonResponse(context)
    else:
        return JsonResponse({'error': 'true', 'message': 'invalid requests'})

# ! delete employee


def delete_employee(request):
    if request.method == 'POST':
        uid = request.POST.get('user_id')
        try:
            Employee.objects.get(id=uid).delete()
        except:
            pass
        return JsonResponse({'error': 'false', 'message': 'data deleted successfully'})
    else:
        return JsonResponse({'error': 'true', 'message': 'invalid requests'})

# !create or update services


def create_or_update_service(request):
    if request.method == "POST":
        sname = request.POST.get('s_name')
        desc = request.POST.get('desc')
        doc = request.POST.get('doc')
        sid = request.POST.get('sid')
        try:
            if sid is not None:
                raise ValueError
            _x, _ = Service.objects.get_or_create(
                name=sname, desc=desc, doc=doc)
            _s = "service created successfully"
        except:
            _x = Service.objects.get(id=sid)
            _x.name = sname
            _x.desc = desc
            _x.doc = doc
            _x.save()
            _s = "Service updated Successfully"

        context = {
            'error': 'false',
            'data': {
                'id': _x.pk,
                'name': _x.name,
                'description': _x.desc,
                'documents': _x.doc

            },
            'mesaage': _s

        }
        return JsonResponse(_s)

    else:
        return JsonResponse({'error': 'true', 'message': 'invalid requests'})

# !delete service


def delete_service(request):
    if request.method == 'POST':
        uid = request.POST.get('s_id')
        try:
            Service.objects.get(id=uid).delete()
        except:
            pass
        return JsonResponse({'error': 'false', 'message': 'Service deleted successfully'})
    else:
        return JsonResponse({'error': 'true', 'message': 'invalid requests'})

# ! get data for the update


def get_service_data(request, id):
    try:
        _x = Service.objects.get(id=id)

        context = {
            'error': 'false',
            'data': {
                'id': _x.pk,
                'name': _x.name,
                'description': _x.desc,
                'documents': _x.doc

            }
        }
    except:
        context = {
            'error': 'true',
            'message': 'invalid service id'
        }
    return JsonResponse(context)

# !sample view


def employee_table(request):
    context = {
        'data': Employee.objects.all()
    }
    return render(request, 'table.html', context)


def employee_manage(request):
    return render(request, 'index.html')
# ! sample ends


# ! chat request bridge for users not for Employees
def hitSupport(request, sid):
    # x =
    if request.session.get('room') is None and request.session.get('sid') != sid:
        support = support.objects.get(id=sid)
        n = str(uuid4())
        n = n.replace('-', "")
        Room.objects.get_or_create(
            rid=n, created_by=request.user, service_id=sid)
        request.session['room'] = n
        request.session['sid'] = sid
    else:
        try:
            _xr = Room.objects.filter(rid=request.session['room'])[0]
            if _xr.room_status != 0:
                support = support.objects.get(id=sid)
                n = str(uuid4())
                n = n.replace('-', "")
                Room.objects.get_or_create(
                    rid=n, created_by=request.user, service_id=sid)
                request.session['room'] = n
                request.session['sid'] = sid
            else:
                raise ValueError
        except:
            pass

    context = {
        'room': request.session['room'],
        'service_id': request.session['sid']
    }

    return JsonResponse(context)

# ! pending Chats For specific services


def PendingChat(request):
    data = Room.objects.filter(
        counter__isnull=True, room_status='0', service_id=request.user.employee.counter.service_id)
    # print(request.user.employee.counter.service_id)
    li = []
    for i in data:
        li.append({
            'id': i.id,
            'room_id': i.rid,
            'created_by': i.created_by.username,
            'created_at': i.created_at,
            'message': i.get_latest_msg,

        })

    return JsonResponse({'error': 'falsecx', 'data': li})

#! accepted chats for employee


def AcceptedChats(request):
    data = Room.objects.filter(
        counter__isnull=False, counter__employee__user_id=request.user.id, room_status='0', service_id=request.user.employee.counter.service_id)
    li = []
    for i in data:
        li.append({
            'id': i.id,
            'room_id': i.rid,
            'created_by': i.created_by.username,
            'created_at': i.created_at,
            'message': i.get_latest_msg,

        })

    return JsonResponse({'data': li})


# def roomChat(request, room_id):

    # return HttpResponse(request,)


# ! counter create or update


def counter_create_or_update(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        sid = request.POST.get('service_id')
        eid = request.POST.get('employee_id')
        c_id = request.POST.get('c_id')
        if c_id is None:
            _x = Counter.objects.create(
                name=name, service_id=sid, employee_id=eid)
            status = "Counter created successfully"
        else:
            _x = Counter.objects.get(id=c_id)
            _x.name = name
            _x.service_id = sid
            _x.employee_id = eid
            _x.save()
            status = "Counter Updated sucessfully"

        context = {
            'id': _x.id,
            'name': _x.name,
            'service': _x.service.name,
            'employee': _x.employee.user.username

        }
        return JsonResponse({'error': 'false', 'data': context})
    else:
        return JsonResponse({'error': 'true', 'message': 'invalid request'})

# !get counter data for update


def get_counter_data(request, id):
    try:
        _x = Counter.objects.get(id=id)

        context = {
            'error': 'false',
            'data': {
                'id': _x.pk,
                'name': _x.name,
                'service': {
                    'id': _x.service.pk,
                    'name': _x.service.name
                },
                'employee': {
                    'id': _x.employee.pk,
                    'id': _x.employee.user.username,
                }

            }
        }
        # ? if user id does not exist may couse error
    except:
        context = {
            'error': 'true',
            'message': 'invalid Counter id'
        }
    return JsonResponse(context)

#! delete counter


def delete_counter(request):
    if request.method == 'POST':
        uid = request.POST.get('c_id')
        try:
            Counter.objects.get(id=uid).delete()
        except:
            pass
        return JsonResponse({'error': 'false', 'message': 'Counter deleted successfully'})
    else:
        return JsonResponse({'error': 'true', 'message': 'invalid requests'})

# !my team


def my_team(request):
    # ! need to add complany based filter
    _x = Employee.objects.filter(status="0").exclude(user_id=request.user.id)
    _li = []
    for i in _x:
        _li.append({
            'id': i.pk,
            'username': i.user.username,
            'email': i.user.email,
            'status': i.status,
            'joined_date': i.j_date
        })
    return JsonResponse({'error': 'false', 'data': _li})

# ! employees in my company


def my_employee(request):
    # ! need to add complany based filter
    _x = Employee.objects.all()
    _li = []
    for i in _x:
        _li.append({
            'id': i.pk,
            'username': i.user.username,
            'email': i.user.email,
            'status': i.status,
            'joined_date': i.j_date
        })
    return JsonResponse({'error': 'false', 'data': _li})
