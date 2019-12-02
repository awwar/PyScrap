# coding=utf-8
from rules.otherrules import RememberRule, RemapRule


def rule(function):
    def wrapper(self, *args, **kvargs):
        self.rules.append(function(self, *args, **kvargs))
        return self

    return wrapper


class BaseParser:

    def __init__(self):
        self.rules = []
        self.stop = False
        self.selected = []
        self.rememberrule = RememberRule()
        self.remaprule = RemapRule()

    @rule
    def remap(self, remaper):
        return self.remaprule.make(remaper)

    @rule
    def remember(self, name, value):
        return self.rememberrule.make(name, value)
