from django.forms.boundfield import BoundField
from django.forms.widgets import Widget, TextInput, CheckboxInput
from django.utils.functional import Promise
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# from chp.components import *
from chp.store import (create_store, render_app)
from chp.mdc.components import *


"""
Boundfield has the following methods to render an HTML widget
using the template engine:
    def __str__(self):
        """ """Render this field as an HTML widget.""" """
        if self.field.show_hidden_initial:
            return self.as_widget() + self.as_hidden(only_initial=True)
        return self.as_widget()

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        """ """
        Render the field by rendering the passed widget, adding any HTML
        attributes passed as attrs. If a widget isn't specified, use the
        field's default widget.
        """ """
        widget = widget or self.field.widget
        if self.field.localize:
            widget.is_localized = True
        attrs = attrs or {}
        attrs = self.build_widget_attrs(attrs, widget)
        if self.auto_id and 'id' not in widget.attrs:
            attrs.setdefault('id', self.html_initial_id if only_initial else self.auto_id)
        return widget.render(
            name=self.html_initial_name if only_initial else self.html_name,
            value=self.value(),
            attrs=attrs,
            renderer=self.form.renderer,
        )

    def build_widget_attrs(self, attrs, widget=None):
        widget = widget or self.field.widget
        attrs = dict(attrs)  # Copy attrs to avoid modifying the argument.
        if widget.use_required_attribute(self.initial) and self.field.required and self.form.use_required_attribute:
            attrs['required'] = True
        if self.field.disabled:
            attrs['disabled'] = True
        return attrs

We need to use similar to get the attrs for 'required', etc.

Alternatively, create custom MdcWidgets and override the widget.render()?

Refactor functions here to classes to support code reuse.
"""


class ChpWidgetMixin:
    chp_widget = None

    def __init__(self, attrs=None, **kwargs):
        self.label = kwargs.pop("label", None)
        if attrs is not None:
            attrs = attrs.copy()
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        """Build a context and render the widget as a component."""
        context = self.get_context(name, value, attrs)
        context['widget'].update(
            {'label': self.label,
             'id_for_label':
                self.id_for_label(context['widget']['attrs']['id'])
             })
        # return self._render(self.template_name, context, renderer)
        return self.chp_render(context)

    def chp_render(self, context):
        raise NotImplementedError


class MdcCheckboxInput(ChpWidgetMixin, CheckboxInput):

    def chp_render(self, context):
        ast_checkbox = Checkbox(
            context['widget']['attrs']['checked'],
            context['widget']['attrs']['id'],
            context
            )

        children = [ast_checkbox,
                    MdcLabelWidget(context)
                    ]
        return FormField(children)


def MdcCheckbox(field):
    # code taken from Boundfield.label_tag()
    label_suffix = (field.field.label_suffix
                    if field.field.label_suffix is not None
                    else (field.form.label_suffix
                          if hasattr(field, "form") else ""))
    contents = field.label
    if label_suffix and contents and contents[-1] not in _(':?.!'):
        label = format_html('{}{}', contents, label_suffix)

    return field.as_widget(MdcCheckboxInput(label=label))


def MdcInput(field):
    if field.mdc_type == "MDCDateField":
        input_type = "date"
    else:
        input_type = "text"

    ast = Input(input_type, field.auto_id)

    # widget formatted value
    value = field.field.widget.format_value(field.value())
    if not (value == '' or value is None):
        ast["props"].append(
            cp("value", value)
        )
    # widget-level attrs
    for (key, value) in field.field.widget.attrs.items():
        ast["props"].append(
            cp(key, value)
        )

    return ast


def DjLabel(field):
    label = field.label
    # cast gettext_lazy strings so they are recognised by AST renderer
    if isinstance(label, Promise):
        label = conditional_escape(label)

    context = {
        "input_type": field.field.widget.input_type,
        "id_for_label": field.id_for_label,
        "label": label,
    }

    return Label(label, context["id_for_label"], context)


def MdcLabelWidget(context):
    label = context['widget']['label']
    # render gettext_lazy strings so they are recognised by AST renderer
    if isinstance(label, Promise):
        label = str(label)

    el_for = context['widget']['id_for_label']
    el_context = {}
    el_context["input_type"] = context['widget']['type']

    return Label(label, el_for, el_context)


def MdcTextField(field):
    if not hasattr(field, 'mdc_type'):
        field.mdc_type = 'MDCTextField'

    children = [
        MdcInput(field),
        DjLabel(field),
        LineRipple(),
    ]
    return InputField(field.field.widget.input_type, children)


def MdcDateField(field):
    if not hasattr(field, 'mdc_type'):
        field.mdc_type = 'MDCDateField'
    return MdcTextField(field)
