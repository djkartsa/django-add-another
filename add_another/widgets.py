# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _


class PopUpBaseWidget(object):
    """
    A widget mixin that adds an "add new" plus icon with a link to open a pop-up window for creating a new object.

    :keyword model: The model class of which a new instance will be created.
    :keyword add_another_template: Template file name for rendering the link.
    :keyword add_another_url: Url to the view that will render and process the popup form.
    :keyword add_another_title_text: Text that will be put in the link's title attribute.
    """

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        self.template = kwargs.pop('add_another_template', 'add_another/addnew.html')
        self.add_another_url = kwargs.pop('add_another_url', None)
        self.title_text = kwargs.pop('add_another_title_text', _(u"Create new"))
        super(PopUpBaseWidget, self).__init__(*args, **kwargs)

    def render(self, name, *args, **kwargs):
        html = super(PopUpBaseWidget, self).render(name, *args, **kwargs)
        if hasattr(self, 'attrs') and (self.attrs.get('disabled') or self.attrs.get('readonly')):
            return html

        if not self.model:
            self.model = name

        if self.add_another_url is None:
            self.add_another_url = reverse('add_another', kwargs={'model_name': getattr(self.model, '__name__', name)})

        popupplus = render_to_string(self.template, {'field': name,
                                                     'add_another_url': self.add_another_url,
                                                     'title_text': self.title_text})
        return popupplus + html

    class Media:
        js = (
            'js/add_another.js',
        )
