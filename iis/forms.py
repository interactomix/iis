from flask_wtf import Form
from wtforms.fields import RadioField

import iis.util.process as process


def process_selection_form(process: process.AbstractProcess=None) -> type:
    """Return a form class for process inheriting from FlaskForm"""
    if process is None:
        return AvailableDataForm

    __bases__ = (Form,)
    __dict__ = {}

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    next_process_choices = []
    for ident in process.list_next_nodes():
        next_process = process.next_node(ident)
        next_process_choices.append((ident, next_process.name))

    __dict__["next_process_choice"] = RadioField(choices=next_process_choices)
    __dict__["__init__"] = __init__

    __name__ = "Process" + process._id + "Form"
    return type(__name__, __bases__, __dict__)


class AvailableDataForm(Form):
    available_data = RadioField(
        choices=[(member, name) for name, member in
                 process.DataType.__members__.items()]
    )
