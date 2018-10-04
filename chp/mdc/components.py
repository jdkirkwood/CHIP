
from .. import components as chp

from ..pyreact import (ce, cp)

MDC_TYPE_MAP = {
    "text": {
        "class": "mdc-text-field",
        "init": "MDCTextField",
        },
    "date": {
        "class": "mdc-date-field",
        "init": "MDCTextField",
        },
    "select": {
        "class": "mdc-select",
        "init": "MDCSelect",
        },
}


def Div(props=[], children=[]):
    return chp.Div(props, children)


def Grid(children=[]):
    props = [
        cp('class', 'mdc-layout-grid')
    ]
    return Div(props, children)


def Row(children=[]):
    props = [
        cp('class', 'mdc-layout-grid__inner')
    ]
    return Div(props, children)


def Cell(children=[]):
    props = [
        cp('class', 'mdc-layout-grid__cell')
    ]
    return Div(props, children)


def Form(children, action="#", method="POST"):
    ast = chp.Form(children, action, method)
    ast["props"].append(
        cp('class', 'mdc-layout-grid__cell')
    )
    return ast


def FormField(children):
    props = [
        cp("class", "mdc-form-field mdc-form-field--align-end"),
        cp("data-mdc-auto-init", "MDCFormField"),
    ]
    return Div(props, children)


def LineRipple():
    return Div([cp("class", "mdc-line-ripple")], [])


def Label(label, el_for=None, context={}):
    ast = chp.Label(label, el_for)

    if context.get("input_type", "text") not in ['checkbox']:
        ast["props"].append(
            cp("class", "mdc-floating-label")
        )

    return ast


def Input(el_type="text", el_id=None):
    ast = chp.Input(el_type, el_id)

    ast["props"].append(
        cp("class", "mdc-text-field__input"),
    )
    return ast


def Checkbox(is_checked=False, el_id=None, context={}):
    ast_input = chp.Checkbox(is_checked, el_id)

    ast_input["props"].append(
        cp('class', 'mdc-checkbox__native-control')
    )

    props = [
        cp("class", "mdc-checkbox"),
        cp("data-mdc-auto-init", "MDCCheckbox"),
    ]
    children = [
        ast_input,
        Div([cp("class", "mdc-checkbox__background")],
            []
            ),
    ]
    ast_field = Div(props, children)

    return ast_field


def InputField(el_type="text", children=[]):
    mdc_type = MDC_TYPE_MAP[el_type]
    props = [
        cp("class", mdc_type["class"]),
        cp("data-mdc-auto-init", mdc_type["init"]),
    ]
    return Div(props, children)


def SubmitButton(name, on_click):
    props = [
        cp('onclick', on_click)
    ]
    return Button(props, name)
