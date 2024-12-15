from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Expense


class ExpenseManagerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="testuser@example.com")

        self.expense1 = Expense.objects.create(
            user=self.user,
            title="Groceries",
            amount=50.00,
            date="2024-12-01",
            category="Food"
        )
        self.expense2 = Expense.objects.create(
            user=self.user,
            title="Bus Ticket",
            amount=20.00,
            date="2024-12-02",
            category="Travel"
        )
        self.expense3 = Expense.objects.create(
            user=self.user,
            title="Electricity Bill",
            amount=100.00,
            date="2024-12-10",
            category="Utilities"
        )
        self.expense4 = Expense.objects.create(
            user=self.user,
            title="Water Bill",
            amount=100.00,
            date="2024-12-10",
            category="Utilities"
        )

        # Base endpoints
        self.user_url = reverse('user-list')
        self.expense_url = reverse('expense-list')

    def test_create_user(self):
        response = self.client.post(self.user_url, {"username": "newuser", "email": "newuser@example.com"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_list_users(self):
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_expense(self):
        response = self.client.post(self.expense_url, {
            "user": self.user.id,
            "title": "Lunch",
            "amount": 15.00,
            "date": "2024-12-15",
            "category": "Food"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 5)

    def test_list_expenses(self):
        response = self.client.get(self.expense_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_retrieve_expense(self):
        response = self.client.get(reverse('expense-detail', args=[self.expense1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Groceries")

    def test_update_expense(self):
        response = self.client.put(reverse('expense-detail', args=[self.expense1.id]), {
            "user": self.user.id,
            "title": "Supermarket Shopping",
            "amount": 60.00,
            "date": "2024-12-01",
            "category": "Food"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.expense1.refresh_from_db()
        self.assertEqual(self.expense1.title, "Supermarket Shopping")

    def test_delete_expense(self):
        response = self.client.delete(reverse('expense-detail', args=[self.expense1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Expense.objects.count(), 3)

    def test_list_by_date_range(self):
        response = self.client.get(reverse('expense-date_range'), {
            "user": self.user.id,
            "start_date": "2024-12-01",
            "end_date": "2024-12-05"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_category_summary(self):
        response = self.client.get(reverse('expense-category_summary'), {
            "user": self.user.id,
            "month": "12"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        summary = {item['category']: item['total'] for item in response.data}
        self.assertEqual(summary["Food"], 50.00)
        self.assertEqual(summary["Travel"], 20.00)
        self.assertEqual(summary["Utilities"], 200.00)

