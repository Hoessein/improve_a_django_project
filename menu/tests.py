from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from .models import Menu, Item, Ingredient
from django.core.urlresolvers import reverse
from .forms import MenuForm


class MenuModelTests(TestCase):

    def test_menu_creation(self):
        """Tests if Menu object can be created"""
        menu = Menu.objects.create(
            season='Summer',
            created_date=timezone.now(),
            expiration_date=datetime.now()
        )
        self.assertEqual(str(menu), menu.season)
        now = timezone.now()
        self.assertLess(menu.created_date, now)


class ItemModelTests(TestCase):

    def test_item_creation(self):
        """Tests if Item object can be created"""
        item = Item.objects.create(
            name='Item',
            description='Greatest',
            standard=False,
            chef=User.objects.create(username='AOC')
        )
        self.assertEqual(str(item), item.name)


class IngredientModelTests(TestCase):

    def test_ingredient_creation(self):
        """Tests if Ingredient object can be created"""
        ingredient = Ingredient.objects.create(
            name='Ciara'
        )

        self.assertEqual(str(ingredient), ingredient.name)


class MenuViewsTests(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(
            season='Summer',
        )

        self.item = Item.objects.create(
            name='Item',
            description='Greatest',
            standard=False,
            chef=User.objects.create(username='AOC')
        )

        self.ingredient = Ingredient.objects.create(
            name='Ciara'
        )

    def test_menu_list_view(self):
        """tests the menu list view"""
        resp = self.client.get(reverse('menu:menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_list.html')
        self.assertIn(self.menu, resp.context['menus'])

    def test_menu_detail_view(self):
        """Tests the menu detail view"""
        resp = self.client.get(reverse('menu:menu_detail',
                                       kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Summer')
        self.assertEqual(self.menu, resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')

    def test_detail_404(self):
        """Tests if 404 is generated if object doesn't exist"""
        resp = self.client.get(reverse('menu:menu_detail', kwargs={'pk': 984}))
        self.assertEqual(resp.status_code, 404)

    def test_create_menu_view(self):
        """Tests if a menu object can be created"""
        resp = self.client.get(reverse('menu:create_menu'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual('Create Menu', resp.context['title'])
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')

    def test_edit_menu_view(self):
        """"Tests if a menu object can be edited"""
        resp = self.client.get(reverse('menu:edit_menu', kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual('Edit Menu', resp.context['title'])
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')

    def test_item_detail_view(self):
        """Tests the item detail view"""
        resp = self.client.get(reverse('menu:item_detail', kwargs={'pk': self.item.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/detail_item.html')


class MenuFormTests(TestCase):
    def test_menu_form(self):
        """tests the menu form"""
        test_user = User.objects.create_user(
            username='testing',
            password='123456'
        )

        test_item = Item.objects.create(
            name='Hoessein',
            description='Whut',
            chef=test_user
        )

        form_data = {
            'season': 'Winter',
            'items': [test_item.id],
            'expiration_date': '03/20/2020'
        }

        form = MenuForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_clean_season_field(self):
        """Tests if validation error is raised for the season field"""
        test_user = User.objects.create_user(
            username='testing',
            password='123456'
        )

        test_item = Item.objects.create(
            name='Hoessein',
            description='Whut',
            chef=test_user
        )

        form_data = {
            'season': 'Char',
            'items': [test_item.id],
            'expiration_date': '03/20/9999'
        }

        form = MenuForm(data=form_data)
        self.assertFalse(form.is_valid())
