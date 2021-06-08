from django.urls import path
from .views import *

# ! url patterns for counter module
urlpatterns = [
    path('user/search/<name>/', get_user_by_name, name="search_employee"),
    # ? employeee
    path('employee/<id>/', get_employee_data, name="get_employee_data"),
    path('employee/create_or_update/', create_or_update_employee,
         name="create_or_update_employee"),
    path('employee/delete/', delete_employee, name="delete_employee").
    path('company/employees/', my_employee, name="employee_list"),
    path('employee/my_team/', my_team, name="my_team"),
    # ? service
    path('service/create_or_update/', create_or_update_service,
         name="create_or_update_service"),
    path('service/<id>', get_service_data, name="get_service_data"),
    path('service/all/', AllService, name="all_services"),
    path('service/delete/', delete_service, name="delete_service"),
    # ? Counter
    path('counter/create_or_update/', counter_create_or_update,
         name="counter_create_or_update"),
    path('counter/<id>', get_counter_data, name="get_counter_data"),
    path('counter/all/', Allcounters, name="all_counters"),
    path('counter/delete/', delete_counter, name="delete_counter"),
    # ? chat room related
    path('service/support/hit/', hitSupport, name="chat_bridge"),
    path('support/pendings/', PendingChat, name="pending_support_chats"),
    path('support/accepted/', AcceptedChats, name="accepted_chats"),
    path('support/accept/<room_id>/', RoomAccept, name="accept_chat"),



]
