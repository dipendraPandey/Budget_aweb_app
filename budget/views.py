from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.http import HttpResponseRedirect, HttpResponse
from .models import Project, Category, Expense
from django.views.generic import CreateView
from .forms import ExpenseForm
import json 
# Create your views here.
def project_list(request):
	projects = Project.objects.all()[::-1]
	context = {}
	context['project_list']=projects 
	return render(request, 'budget/project_list.html',context)



def project_detail(request, slug):
	project = get_object_or_404(Project, slug=slug)
	if request.method == 'GET':
		category_list = Category.objects.filter(project=project)
		expense_list = project.expenses.all()
		context = {}
		context['project']=project
		context['category_list']=category_list
		context['expense_list']=expense_list
		return render(request, 'budget/project_detail.html', context)
	elif request.method == 'POST':
		# process form
		form = ExpenseForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			amount = form.cleaned_data['amount']
			category_name = form.cleaned_data['category']
			category = get_object_or_404(Category, project=project, name = category_name)
			Expense.objects.create(
				project=project,
				title = title,
				amount= amount,
				category = category).save()
	elif request.method =='DELETE':
		id = json.loads(request.body)['id']
		expense = get_object_or_404(Expense, id=id)
		expense.delete()
		return redirect('budget:detail', slug=slug)
	return redirect('budget:detail', slug=slug)

class ProjectCreateView(CreateView):
	model = Project
	template_name = 'budget/project_add.html'
	fields = ('name', 'budget')


	def form_valid(self, form):
		self.objects = form.save(commit=False)
		self.objects.save()
		categories = self.request.POST['categoriesString'].split(',')
		print(categories)

		for category in categories:
			Category.objects.create(
				project= Project.objects.get(id=self.objects.id),
				name = category
				)
		return HttpResponseRedirect(self.get_success_url())


	def get_success_url(self):
		return redirect(slugify(self.request.POST['name']))