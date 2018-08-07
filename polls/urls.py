from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # /polls/5/
    path('<int:pk>/', views.DetailView.as_view(), name="detail"),
    # /polls/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name="results"),
    # /polls/5/vote/
    path('<str:question_id>/vote/', views.vote, name='vote'),

    path('search', views.QuestionSearchListView.as_view(), name='question_search_list_view'),

    path('api/data', views.get_data, name='api-data'),
    path('api/chart/data/<int:question_id>', views.ChartData.as_view()),
]