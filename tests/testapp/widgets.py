# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from add_another.widgets import PopUpBaseWidget


class FilteredMultipleSelectWithPopUp(PopUpBaseWidget, FilteredSelectMultiple):
    pass


class MultipleSelectWithPopUp(PopUpBaseWidget, forms.SelectMultiple):
    pass


class SelectWithPopUp(PopUpBaseWidget, forms.Select):
    pass
