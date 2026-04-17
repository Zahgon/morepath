"""This module contains default Morepath configuration shared by
all Morepath applications. It is the only part of the Morepath
implementation that uses directives like user of Morepath does.

It uses Morepath directives to configure:

* view predicates (for model, request method, etc), including
  what HTTP errors should be returned when a view cannot be matched.

* converters for common Python values (int, date, etc)

* a tween that catches exceptions raised by application code
  and looks up an exception view for it.

* a default exception view for HTTP exceptions defined by
  :mod:`webob.exc`, i.e. subclasses of :class:`webob.exc.HTTPException`.

Should you wish to do so you could even override these directives in a
subclass of :class:`morepath.App`. We do not guarantee we won't break
your code with future version of Morepath if you do that, though.
"""

import re
from datetime import date, datetime
from time import mktime, strptime

from webob.exc import (
    HTTPBadRequest,
    HTTPException,
    HTTPMethodNotAllowed,
    HTTPNotFound,
    HTTPOk,
    HTTPRedirection,
)

from reg import ClassIndex, KeyIndex

from .app import App
from .converter import IDENTITY_CONVERTER, Converter


@App.predicate(App.get_view, name="model", default=None, index=ClassIndex)
def model_predicate(self, obj, request):
    """match model argument by class.

    Predicate for :meth:`morepath.App.view`.
    """
    return obj.__class__


@App.predicate_fallback(App.get_view, model_predicate)
def model_not_found(self, obj, request):
    """if model not matched, HTTP 404.

    Fallback for :meth:`morepath.App.view`.
    """
    raise HTTPNotFound()


@App.predicate(
    App.get_view, name="name", default="", index=KeyIndex, after=model_predicate
)
def name_predicate(self, obj, request):
    """match name argument with request.view_name.

    Predicate for :meth:`morepath.App.view`.
    """
    return request.view_name


@App.predicate_fallback(App.get_view, name_predicate)
def name_not_found(self, obj, request):
    """if name not matched, HTTP 404.

    Fallback for :meth:`morepath.App.view`.
    """
    raise HTTPNotFound()


@App.predicate(
    App.get_view,
    name="request_method",
    default="GET",
    index=KeyIndex,
    after=name_predicate,
)
def request_method_predicate(self, obj, request):
    """match request method.

    Predicate for :meth:`morepath.App.view`.
    """
    return request.method


@App.predicate_fallback(App.get_view, request_method_predicate)
def method_not_allowed(self, obj, request):
    """if request predicate not matched, method not allowed.

    Fallback for :meth:`morepath.App.view`.
    """
    raise HTTPMethodNotAllowed()


@App.converter(type=int)
def int_converter():
    """Converter for int."""
    pass


@App.converter(type=str)
def unicode_converter():
    """Converter for text."""
    pass


def date_decode(s):
    pass


def date_encode(d):
    pass


@App.converter(type=date)
def date_converter():
    """Converter for date."""
    pass


def datetime_decode(s):
    pass


def datetime_encode(d):
    pass


@App.converter(type=datetime)
def datetime_converter():
    """Converter for datetime."""
    pass


@App.tween_factory()
def excview_tween_factory(app, handler):
    """Exception views.

    If an exception is raised by application code and a view is
    declared for that exception class, use it.

    If no view can be found, raise it all the way up -- this will be a
    500 internal server error and an exception logged.
    """
    pass


@App.tween_factory(over=excview_tween_factory)
def poisoned_host_header_protection_tween_factory(app, handler):
    """Protect Morepath applications against the most basic host header
    poisoning attacts.

    The regex approach has been copied from the Django project. To find more
    about this particular kind of attack have a look at the following
    references:

    * https://www.skeletonscribe.net/2013/05/practical-http-host-header-attacks.html
    * https://www.djangoproject.com/weblog/2012/dec/10/security/
    * https://github.com/django/django/commit/77b06e41516d8136b56c040cba7e235b

    """
    pass


@App.view(model=HTTPException)
def standard_exception_view(self, request):
    """We want the webob standard responses for any webob-based HTTP exception.

    Applies to subclasses of :class:`webob.HTTPException`.
    """
    pass
