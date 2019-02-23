from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from .models import Menu, Item, Ingredient
from django.core.urlresolvers import reverse
from .forms import MenuForm
import pdb



class MenuModelTests(TestCase):

    def test_menu_creation(self):
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
        item = Item.objects.create(
            name='Item',
            description='Greatest',
            standard=False,
            chef=User.objects.create(username='AOC')
        )
        self.assertEqual(str(item), item.name)


class IngredientModelTests(TestCase):

    def test_ingredient_menu(self):
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
        """tests the home view"""
        resp = self.client.get(reverse('menu:menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_list.html')
        self.assertIn(self.menu, resp.context['menus'])
        # self.assertContains(resp, 'Search')
        # self.assertContains(resp, self.mineral)

    def test_menu_detail(self):
        resp = self.client.get(reverse('menu:menu_detail',
                                       kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Summer')
        self.assertEqual(self.menu, resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')

    def test_detail_404(self):
        resp = self.client.get(reverse('menu:menu_detail', kwargs={'pk': 984}))
        self.assertEqual(resp.status_code, 404)

    def test_create_menu(self):
        # self.client.login(username='testing', password='123456')
        resp = self.client.get(reverse('menu:create_menu'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual('Create Menu', resp.context['title'])
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')

    def test_edit_menu(self):
        resp = self.client.get(reverse('menu:edit_menu', kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual('Edit Menu', resp.context['title'])
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')

    def test_item_detail(self):
        resp = self.client.get(reverse('menu:item_detail', kwargs={'pk': self.item.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/detail_item.html')

class MenuFormTests(TestCase):
    def test_menu_form(self):
        test_user = User.objects.create_user(username='testing', password='123456')
        test_item = Menu.objects.create(season='Dudjjud')

        form_data = {'season': 'Winter',
            'items': test_item.id,
            'expiration_date': '03/20/2020'
        }
        form = MenuForm(data=form_data)
        print(form.errors)
        pdb.set_trace()
        self.assertTrue(form.is_valid())


