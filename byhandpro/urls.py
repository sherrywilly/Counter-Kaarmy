
from django.contrib import admin
from django.urls import path
from counter.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('table/', employee_table, name='table'),
    path('', employee_manage, name='manage'),
    path('test/', PendingChat, name='manage'),
    path('my_team/', my_team, name='manage'),
    # path('<name>/', get_user_by_name),
    # path('', create_or_update_employee),
    # path('get/<int:id>', get_employee_data),
]
