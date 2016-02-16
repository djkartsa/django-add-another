# -*- coding: utf-8 -*-
from string import capitalize

from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils.html import escape

from forms import get_model_form, normalize_model_name


class AddAnotherMixin(object):
    """A mixin that is intended to be used with a CreateView that renders and processes the add another popup."""

    template_name = 'add_another/popup.html'
    success_url_base = reverse_lazy('add_another_success')
    form_title = None
    show_form_title = True

    def get_context_data(self, **kwargs):
        context = super(AddAnotherMixin, self).get_context_data(**kwargs)
        if self.show_form_title:
            form_title = self.get_form_title()
            if form_title:
                context['form_title'] = form_title
            else:
                form = context.get('form')
                if form:
                    model = form._meta.model
                    if model:
                        context['form_title'] = capitalize(model._meta.verbose_name)
        return context

    def get_form_title(self):
        return self.form_title

    def get_success_url(self):
        if getattr(self, 'object', None):
            return "%s?obj_pk=%s&obj=%s" % (self.success_url_base, escape(self.get_pk_value() or self.object._get_pk_val()), escape(self.get_label() or self.object))
        raise ImproperlyConfigured("The view must create an object before success.")

    def get_label(self):
        """An optional method to customize the label injected to and displayed in the parent window select box."""
        return None

    def get_pk_value(self):
        """An optional method to customize the pk value injected to the parent window select box."""
        return None


def add_new_model(request, model_name, form=None):
    normal_model_name = normalize_model_name(model_name)
    print normal_model_name

    if not form:
        form = get_model_form(normal_model_name)

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            try:
                new_obj = form.save()
            except forms.ValidationError:
                new_obj = None

            if new_obj:
                return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %
                    (escape(new_obj._get_pk_val()), escape(new_obj))
                )

    else:
        form = form()

    page_context = {'form': form, 'field': normal_model_name}
    return render(request, 'add_another/popup.html', page_context)


def add_another_success(request, template='add_another/success.html'):
    """
    The view that can be used to display the success page for add another popup.

    By default a javascript will be rendered that will close the popup and populate
    the parent window's select input with the newly added object.
    """
    obj_pk = request.GET.get('obj_pk', None)
    obj = request.GET.get('obj', None)
    if obj_pk and obj:
        return render(request, template, {'obj_pk': escape(obj_pk), 'obj': escape(obj)})
    raise Http404
