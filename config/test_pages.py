import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from budgets.models import Budget
from categories.models import Category
from notifications.models import Notification


class PageAccessTests(TestCase):
    pages = ["budgets:list", "recurring:list", "wishlist:list", "notifications:list"]

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="pageuser", password="testpass123")
        self.other = User.objects.create_user(username="otherpage", password="testpass456")

    def test_login_required(self):
        for name in self.pages:
            with self.subTest(page=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertRedirects(
                    response, f"{reverse('users:login')}?next={url}"
                )

    def test_pages_load_when_logged_in(self):
        self.client.force_login(self.user)
        for name in self.pages:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_budget_page_shows_only_own_budgets(self):
        mine = Category.objects.create(user=self.user, name="Food", color="#F97316")
        theirs = Category.objects.create(user=self.other, name="Food", color="#16A34A")
        Budget.objects.create(user=self.user, category=mine,
                              month=datetime.date(2026, 12, 1),
                              limit_amount=Decimal("100.00"))
        Budget.objects.create(user=self.other, category=theirs,
                              month=datetime.date(2026, 12, 1),
                              limit_amount=Decimal("200.00"))
        self.client.force_login(self.user)
        budgets = self.client.get(reverse("budgets:list")).context["budgets"]
        self.assertEqual({b.user_id for b in budgets}, {self.user.id})
        self.assertEqual(len(budgets), 1)

    def test_mark_all_read(self):
        Notification.objects.create(user=self.user, message="a")
        Notification.objects.create(user=self.other, message="b")
        self.client.force_login(self.user)
        self.client.post(reverse("notifications:mark_all_read"))
        self.assertFalse(Notification.objects.filter(user=self.user, is_read=False).exists())
        self.assertTrue(Notification.objects.filter(user=self.other, is_read=False).exists())