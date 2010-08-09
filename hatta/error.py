#!/usr/bin/python
# -*- coding: utf-8 -*-

import werkzeug


class WikiError(werkzeug.exceptions.HTTPException):
    """Base class for all error pages."""


class ForbiddenErr(WikiError):
    code = 403


class NotFoundErr(WikiError):
    code = 404


class UnsupportedMediaTypeErr(WikiError):
    code = 415


class NotImplementedErr(WikiError):
    code = 501


class ServiceUnavailableErr(WikiError):
    code = 503


