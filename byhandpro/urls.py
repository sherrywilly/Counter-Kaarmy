
from django.contrib import admin
from django.urls import path
from counter.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('<name>/', get_user_by_name),
    path('', create_or_update_employee),
    path('get/<int:id>', get_employee_data),
]
