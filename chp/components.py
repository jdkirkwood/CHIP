from .pyreact import *


def Div(props, children):
    children = children or []
    return ce('div', props, children)


def Button(props, children):
    props = props or []
    props.append(
        cp('type', 'button'))
    children = children or []
    return ce('button', props, children)


def Script(string=""):
    return ce('script', [], string)


def ScriptBefore(children, script_text):
    children = children or []
    script = [Script(script_text)]
    children = script.append(children)
    return Div([], children)


def Form(children, action="#", method="POST"):
    props = [
        cp('action', action),
        cp('method', method),
    ]
    return ce('form', props, children)


def Errors():
    props = []
    children = '''
    '''
    return Div(props, children)


def Input(el_type="text", el_id=None):
    props = [
        cp('type', el_type),
    ]
    if id is not None:
        props.append(
            cp('id', el_id),
        )
    return ce('input', props, [])


def Checkbox(is_checked=False, el_id=None):
    ast = Input("checkbox", el_id)
    if is_checked:
        ast["props"].append(
            cp('checked', "")
        )
    return ast


def Label(label, el_for=None):
    props = []
    if el_for is not None:
        props = [
            cp("for", el_for)
        ]

    return ce('label', props, label)


# def Label(name):
#     def c(context):
#         props = [
#         ]
#         return ce('label', props, context["label"] + " " + name)
#     return c


# def CheckboxField(isChecked):
#     def c(context):
#         children = []
#         props = [
#             cp('class', 'mdc-form-field')
#         ]
#         children.append(Div(
#             [cp("class", "mdc-checkbox")],
#             [
#                 Checkbox(isChecked),
#                 Div(
#                     [cp("class", "mdc-checkbox-background")],
#                     []
#                 ),
#                 Label('Checkbox'),
#                 Label(context["label"])
#             ]
#         ))
#         return Div(props, children)
#     return c
