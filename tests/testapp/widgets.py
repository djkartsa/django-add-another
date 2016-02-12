# -*- coding: utf-8 -*-
from add_another.widgets import PopUpBaseWidget
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms


class FilteredMultipleSelectWithPopUp(PopUpBaseWidget, FilteredSelectMultiple):
    pass


class MultipleSelectWithPopUp(PopUpBaseWidget, forms.SelectMultiple):
    pass


class SelectWithPopUp(PopUpBaseWidget, forms.Select):
    pass