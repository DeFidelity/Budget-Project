from django.test import TestCase,Client
from budget.models import Category, Project, Expense
from django.urls import reverse
import json


class TestViews(TestCase):
    def setup(self):
        self.client = Client()

    def test_list_view_GET(self):
        self.list_url = reverse('list')
        response = self.client.get(self.list_url)

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'budget/project-list.html')

    def test_project_detail_GET(self):
        Project.objects.create(name="to detail",budget=1000)
        detail_url = reverse('detail',args=['to-detail'])

        response = self.client.get(detail_url,args=['build-a-house'])
        print(response)

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'budget/project-detail.html')

    def test_project_detail_POST(self):
        project= Project.objects.create(name='new project',budget=2000)
        Category.objects.create(project=project,name="new-category")
        request_url = reverse('detail',args=['new-project'])

        response = self.client.post(request_url)
        print(response)

    def test_project_create_POST(self):
        project= Project.objects.create(name='new project 2',budget=20000)
        category = Category.objects.create(project=project,name="building blocks")
        request_url = reverse('detail',args=['new-project-2'])

        response = self.client.post(request_url,{
            'title':'new project',
            'amount': 6000,
            'category': 'building blocks'
        })

        self.assertEquals(response.status_code,302)
        self.assertEquals(project.expenses.first().title,'new project')
        self.assertEquals(project.budget_left,14000)

    def test_project_create_POST_with_no_data(self):
        project= Project.objects.create(name='new project 2',budget=20000)
        category = Category.objects.create(project=project,name="building blocks")
        request_url = reverse('detail',args=['new-project-2'])

        response = self.client.post(request_url,)

        self.assertEquals(response.status_code,302)
        self.assertEquals(project.expenses.count(),0)

    def test_project_create_POST_with_wrong_data(self):
        project= Project.objects.create(name='new project 2',budget=20000)
        category = Category.objects.create(project=project,name="building blocks")
        request_url = reverse('detail',args=['new-project-2'])

        response = self.client.post(request_url,{
            'title':'f',
            'amount': 'amount',
            'category': 'no category'
        })

        self.assertEquals(response.status_code,302)

    def test_project_detail_delete_view(self):
        project = Project.objects.create(name='this project',budget=34000)
        category = Category.objects.create(name='buy-block',project=project)
        first_expense = Expense.objects.create(project=project,title='first block',amount=3080, category=category)
        second_expense = Expense.objects.create(project=project,title='roof pan',amount=5680, category=category)
        delete_url = reverse('detail',args=['this-project'])


        response = self.client.delete(delete_url,json.dumps({'id':first_expense.pk}))

        self.assertEquals(response.status_code,204)
        lent = len([p for p in Expense.objects.filter(project=project)])
        self.assertEquals(lent,1)
