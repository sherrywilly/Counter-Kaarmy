
from django.contrib import admin
from django.urls import path, include
from counter.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('table/', employee_table, name='table'),
    path('counter/', include('counter.urls')),
    # path('', employee_manage, name='manage'),

]
