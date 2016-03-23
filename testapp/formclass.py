# -*- coding:utf-8 -*-
"""Form class creation."""
from wtforms import Form, StringField, TextAreaField, validators


class EntryForm(Form):
    """Define EntryForm class."""

    title = StringField('Title', [validators.Length(min=4, max=128,
                                  message='Title must be 4 to 128 characters long.')])
    text = TextAreaField('Content', [validators.Length(min=6,
                                     message='Content must be at least 6 characters.')])
