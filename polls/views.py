#2480678656
#12/2/2000

import os
import operator

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Question, Choice
from django.db.models import Sum, Count
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model

# Create your views here.

class IndexView(generic.ListView):

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    queryset = Choice.objects.values('question_id','question__question_text','question__pub_date').annotate(Sum('votes'), total=Count('question_id')).filter(total__gte=2)
    paginate_by = 3

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super(IndexView, self).get_context_data(**kwargs)
    #     # Add in the publisher
    #     # context['latest_question_list'] = Question.objects.order_by('-pub_date')[:5]
    #     # Choice.objects.annotate(num_books=Sum('votes'))
    #     # print(context)
    #     context.update({'question_with_votes': [(Question.objects.get(pk=each['question']).qu,each['votes']) for each in Choice.objects.values('question').annotate(votes=Sum('votes'))]})
    #     # context['votes'] = Choice.objects.all().filter(question=)
    #     print(context)
    #     return context


    # def get_queryset(self):
    #     # context_object_name = {'latest_question_list':Choice.objects.values('question').annotate(votes=Sum('votes'))}
    #     # questions = Choice.objects.values('question_id','question__question_text','question__pub_date').annotate(Sum('votes'))[:5]
    #     # paginator = Paginator(questions, 3) # < 3 is the number of items on each page
    #     # page = request.Get.get('page') # < Get the page number
    #     #
    #     # questions = paginator.get_page(page) # < New in 2.0
    #     #
    #     # return questions;
    #     return Choice.objects.values('question_id','question__question_text','question__pub_date').annotate(Sum('votes'))

class QuestionSearchListView(generic.ListView):
    paginate_by = 3
    def get_queryset(self):
        result = super(QuestionSearchListView, self).get_queryset()
        return result

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     #output = ', '.join([q.question_text for q in latest_question_list])
#     # return HttpResponse(template.render(context, request))
#     # a shortcut render
#     return render(request, 'polls/index.html', context)



def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    print("===========",question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data) # http response

User = get_user_model()

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None, question_id = False):
        id = question_id
        print(id)
        qs_count = Choice.objects.filter(question_id=id)
        labels = []
        default_items = []
        for c in qs_count:
            i=0;
            labels.insert(i, c.choice_text)
            default_items.insert(i, c.votes)
            i = i + 1;

        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)


class HomeView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'polls/chart.html', {"customers": 10})