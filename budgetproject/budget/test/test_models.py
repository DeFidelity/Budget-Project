from django.test import TestCase, Client
from django.urls import reverse
from budget.models import Project, Category, Expense
from budget.views import project_detail



class TestModels(TestCase):
    def setup(self):
        self.client = Client()
    def test_budget_left_method_in_project_model(self):
        project = Project.objects.create(name='this project',budget=32488)
        category = Category.objects.create(name='first block',project=project)
        first_expense = Expense.objects.create(project=project,title='first block',amount=3080, category=category)
        second_expense = Expense.objects.create(project=project,title='roof pan',amount=5680, category=category)

        self.assertEquals(project.budget_left,23728)

    def test_model_slugify_method_in_project_model(self):
        project = Project.objects.create(name="this is a new housing project", budget=200020)
        self.assertEquals(project.slug,'this-is-a-new-housing-project')

    def test_get_absolute_url_method_in_project_model(self):
        project = Project.objects.create(name="this is a new housing project", budget=200020)
        project_url = reverse('detail',args=['this-is-a-new-housing-project'])

        response = self.client.get(project.get_absolute_url())
        self.assertEquals(response.status_code,301)
