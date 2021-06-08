from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Employee(models.Model):
    E_CHOICE = (('0', 'Online'), ('1', 'Leave'), ('3', 'Resigned'),)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # ! company foreign key is pending to add
    emp_id = models.CharField(
        max_length=50, unique=True, verbose_name="employee id")
    position = models.CharField(max_length=100, verbose_name="job position")
    j_date = models.DateField(verbose_name="joining date")
    status = models.CharField(max_length=10, choices=E_CHOICE, default='1')
    # verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)+" "+self.position


class Service(models.Model):
    # ! company foreign key is pending to add
    name = models.CharField(max_length=200, verbose_name="service name")
    desc = models.TextField(blank=True, null=True, verbose_name="description")
    doc = models.TextField(blank=True, null=True, verbose_name='documents')

    def __str__(self):
        return self.name


class Counter(models.Model):
    name = models.CharField(max_length=200)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    employee = models.OneToOneField(Employee, on_delete=models.DO_NOTHING)


class Room(models.Model):
    ROOM_STATUS = (('0', 'Open'), ('1', 'Closed'))
    rid = models.CharField(max_length=200, unique=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    room_status = models.CharField(
        max_length=30, default='0', choices=ROOM_STATUS)
    counter = models.ForeignKey(
        Counter, on_delete=models.SET_NULL, blank=True, null=True)
    #

    @property
    def get_latest_msg(self):
        try:
            _x = self.thread_set.all()[::-1][0]
            _context = {
                'last_message': _x.msg,
                'author': _x.created_by.username,
                'author_id': _x.created_by.pk,
                'created_at': _x.created_at,
            }
        except:
            _context = {}

        return _context


class Thread(models.Model):
    MSG_TYPE = (('1', 'text'), ('2', 'img'))
    msg = models.TextField(blank=True, null=True)
    msg_type = models.CharField(default='1', choices=MSG_TYPE, max_length=20)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.msg)
