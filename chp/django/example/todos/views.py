import json

from django.utils.safestring import mark_safe
from django.views import generic

from chp.pyreact import (context_middleware, inject_ids, render_element)
from chp.store import Inject_ast_into_DOM

from .components import FormSchema


class TodosView(generic.TemplateView):
    template_name = 'todos.html'

    def body(self):
        is_checked = {
            "name": "hello",
        }
        ctx = {
            "label": "Labelling:",
            "password": "bar",
        }
        store = {
            "name": "this is my first store !!",
            "todos": [
                {
                    "name": "hello",
                    "id": "0",
                },
                {
                    "name": "todo number secondo !!",
                    "id": "1",
                },
            ]
        }
        ast = FormSchema(store, json.dumps(store))
        form = inject_ids(ast)
        app = Inject_ast_into_DOM(form, json.dumps(form))
        html = render_element(app, context_middleware(ctx))
        return mark_safe(html)
