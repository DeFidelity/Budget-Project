from django.test import SimpleTestCase
from budget.views import project_list, ProjectCreateView, project_detail
from django.urls import reverse, resolve

class TestURLS(SimpleTestCase):

    def test_list_url(self):
        self.list_url = reverse('list')
        self.assertEquals(resolve(self.list_url).func,project_list)

    def test_detail_url_resolve(self):
        self.detail_url = reverse('detail',args=['some-slug'])
        print(resolve(self.detail_url))
        self.assertEquals(resolve(self.detail_url).func,project_detail)

    def test_classbased_add_url(self):
        self.add_url = reverse('add')
        self.assertEquals(resolve(self.add_url).func.view_class,ProjectCreateView)
