from lxml import html
import re
from collections import Iterable

class Rule:
    def __init__(self, exequtor, *args, **kvargs):
        self.exequtor = exequtor
        self.args = args
        self.kvargs = kvargs


class Selector:
    def __init__(self, settings):
        self.required = []
        self.default = {}
        if self.notEmpty(settings) and isinstance(settings, dict):
            for key, value in settings.items():
                if key == 'default':
                    self.setDefault(value)
                elif key == 'required':
                    self.setRequired(value)

    def notEmpty(self, var):
        return var or var is not None

    def toList(self, var):
        try:
            iter(var)
        except TypeError:
            var = [var]

        return var

    def setDefault(self, var):
        for key, val in var.items():
            self.default[key] = val

    def setRequired(self, var):
        if var == "*":
            self.required = True
        elif isinstance(var, list) and var:
            self.required = var
        else:
            raise Exception('Unknown required value!')

    def isRequired(self, key):
        return self.required is True or key in self.required

    def after(self, key, selected, handler):
        if self.notEmpty(selected) and handler is not None:
            selected = self.toList(selected)
            new_selected = []
            for select in selected:
                try:
                    new_selected.append(handler(select))
                except Exception as e:
                    print(e)
            selected = new_selected

        if not self.notEmpty(selected):
            try:
                selected = self.default[key]
            except:
                if self.isRequired(key):
                    raise Exception('None value')
        return {key: selected}

    def make(self, *args, **kvargs):
        return Rule(self, *args, **kvargs)


class CSSSelection(Selector):

    def run(self, dom, key, selector, handler):
        selected = dom.cssselect(selector)
        return self.after(key, selected, handler)


class XPATHSelector(Selector):

    def run(self, dom, key, selector, handler):
        selected = dom.xpath(selector)
        return self.after(key, selected, handler)


class RregularExpressionSelector(Selector):

    def run(self, dom, key, selector, handler):
        prog = re.compile(selector)
        text = html.tostring(dom)
        selected = prog.finditer(text, re.MULTILINE)
        return self.after(key, selected, handler)
