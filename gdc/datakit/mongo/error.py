#!/usr/bin/python
# coding=utf-8

class ConnectionPoolOverLoadError(Exception):
    pass


class ConnectionNotInPoolError(Exception):
    pass


class ConnectionNameConflictError(Exception):
    pass


class AlreadyConnectedError(Exception):
    pass


class ClassAttrNameConflictError(Exception):
    pass


class ConnectionNotFoundError(Exception):
    pass
