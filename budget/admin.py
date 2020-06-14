from django.contrib import admin
from .models import Project, Category, Expense
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
	list_display = ['name', 'budget']
	list_filter = ('budget',)
	search_field = ('name')


class CategoryAdmin(admin.ModelAdmin):
	list_display = ['project','name',]
	list_filter = ('project__name',)
	search_field = ('project__name')

class ExpenseAdmin(admin.ModelAdmin):
	list_display = ['project', 'title', 'amount',]
	list_filter = ('project__name',)
	search_field = ('project__name')



admin.site.register(Project,ProjectAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Expense, ExpenseAdmin)