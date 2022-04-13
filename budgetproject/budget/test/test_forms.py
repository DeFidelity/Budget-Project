from django.test import SimpleTestCase
from budget.models import Project, Category, Expense
from budget.forms import ExpenseForm

class TestExpenseForm(SimpleTestCase):
    def test_expense_form_with_correct_data(self):
        form = ExpenseForm(data={
            'title':'this block and cement',
            'amount':10000,
            'category':'building materials'
        })
        self.assertEquals(len(form.errors),0)
        self.assertEquals(form.is_valid(),True)

    def test_expense_form_with_wrong_data(self):
        form = ExpenseForm(data={
            'title':'this block and cement',
            'amount':'ten thousand naira',
            'category':'building materials'
        })
        self.assertEquals(len(form.errors),1)
        self.assertEquals(form.is_valid(),False)
