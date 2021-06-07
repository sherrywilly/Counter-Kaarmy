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


def employee_table(request):
    context = {
        'data': Employee.objects.all()
    }
    return render(request, 'table.html', context)


def employee_manage(request):
    return render(request, 'index.html')


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

    context = {
        'room': request.session['room'],
        'service_id': request.session['sid']
    }

    return JsonResponse(context)


def roomChat(request, sid, room_id):
    pass

    # return HttpResponse(request,)
