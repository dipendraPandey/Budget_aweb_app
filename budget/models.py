from django.db import models
from django.utils.text import slugify
# Create your models here.

class Project(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100, unique=True, blank=True)
	budget =models.IntegerField()

	def __str__(self):
		return self.name

	def save(self, *arg, **kwargs):
		self.slug = slugify(self.name)
		super(Project,self).save(*arg, **kwargs)


	def total_budget_left(self):
		expenses = Expense.objects.filter(project=self)
		total_budget_spend = 0
		for expense in expenses:
			total_budget_spend += expense.amount
		return self.budget - total_budget_spend

	def total_transaction(self):
		expenses = Expense.objects.filter(project=self)
		transaction = len(expenses)
		return transaction

	class Meta:
		verbose_name = 'Project'
		verbose_name_plural = 'Projects'





class Category(models.Model):
	project = models.ForeignKey(Project, on_delete = models.CASCADE)
	name = models.CharField(max_length=100)

	class Meta:
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.name



class Expense(models.Model):
	project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name='expenses')
	title = models.CharField(max_length=100)
	amount = models.DecimalField(max_digits =8, decimal_places=2)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)


	class Meta:
		verbose_name = 'Expense'
		verbose_name_plural = 'Expenses'


	def __str__(self):
		return self.title
