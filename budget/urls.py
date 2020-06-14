from django.urls import path
from .views import project_detail, project_list,ProjectCreateView



app_name = 'budget'


urlpatterns = [
	path('', project_list, name='list'),
	path('add/', ProjectCreateView.as_view(), name='add'),
	path('<slug>/', project_detail, name='detail')

]
