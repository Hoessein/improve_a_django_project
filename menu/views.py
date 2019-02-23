from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone
from operator import attrgetter
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from .models import *
from .forms import *


def menu_list(request):
    """Shows menus which are not expired ordered by creation date."""

    menus = Menu.objects.filter(
        Q(expiration_date__isnull=True) |
        Q(expiration_date__gte=timezone.now())).prefetch_related('items').order_by('created_date')

    return render(request, 'menu/menu_list.html', {'menus': menus})


def menu_detail(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def create_and_edit_menu(request, pk=None):
    if pk:
        menu = get_object_or_404(Menu, pk=pk)
        title = 'Edit Menu'

    else:
        menu = None
        title = 'Create Menu'

    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)

        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()
            form.save_m2m()
            menu.save()
            return redirect('menu:menu_detail', pk=menu.pk)

    else:
        form = MenuForm(instance=menu)
    return render(request, 'menu/menu_edit.html', {'form': form, 'title': title})


def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})
