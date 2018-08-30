from chp.components import *
from chp.store import (create_store, render_app)


def SubmitButton(name, on_click):
    props = [
        cp('onclick', on_click)
    ]
    return Button(props, name)


def TodoItem(name, todo_id):
    on_click = f"store_updates.remove_todo({todo_id})"
    props = [
        cp("id", todo_id),
        cp("style", "margin: 1rem; min-height: 3rem; background-color: rgba(0, 0, 0, 0.2); border: 2px solid black"),
        cp("onclick", on_click),
    ]
    return Div(props, name)


def Input(value):
    on_key_up = "store_updates.update_todo_name()"

    props = [
        cp('type', 'text'),
        cp('onkeyup', on_key_up),
        cp('id', 'myInput'),
        cp('value', value),
    ]
    return ce('input', props, [])


def MdcInput(id, value):
    props = [
        cp("type", "text"),
        cp("id", id),
        cp("class", "mdc-text-field__input"),
        cp("value", value),
    ]
    children = []
    return ce("input", props, children)


def MdcLabel(id, label):
    props = [
        cp("class", "mdc-floating-label"),
        cp("for", id),
    ]
    return ce("label", props, label)


def MdcLineRipple():
    return Div([cp("class", "mdc-line-ripple")], [])


def MdcTextField(id, label, value):
    props = [
        cp("class", "mdc-text-field")
    ]
    children = [
        MdcInput(id, value),
        MdcLabel(id, label),
        MdcLineRipple(),
    ]
    return Div(props, children)


def FormSchema(store_content, store_content_json):
#     store_name = "todoStore"
#     store_change_cb = [
#         render_app(store_name, store_content_json),
#     ]

#     def add_todos():
#         return f"store_updates.add_todo({store_name})"

    def render():
        form = Form([
            Cell([
                Div(
                    [cp("style", "display: grid;")],
                    [
                        MdcTextField("unique-id",
                                     "MDC label",
                                     "field value",
                                     ),
#                         Input(store_content["name"]),
#                         SubmitButton("Submit", add_todos()),
                    ],
                ),
#                 Div(
#                     [cp("style", "height: 5rem")],
#                     "If you type <strong>foo</strong> in the textbox and unfocus, your secret message will appear !!"
#                 ),
#                 Div([cp("id", "demo"), cp("style", "color: red" if store_content["name"] == "foo" else "color: green")], "what color am I ?"),
            ])
        ])

#         todos = []
#         for t in store_content["todos"]:
#             todos.append(TodoItem(t["name"], t["id"]))
# 
#         return Div(
#             [],
#             [
#                 Script(create_store(store_name, store_change_cb, store_content_json)),
#                 form,
#                 Div([], todos),
#             ],
#         )
        return form

    return render()
