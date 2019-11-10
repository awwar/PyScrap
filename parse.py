def rule(function):
    def wrapper(self, *args, **kvargs):
        self.rules.append(function(self, *args, **kvargs))
        return self

    return wrapper

class BaseParser:

    def __init__(self):
        self.rules = []
        self.stop = False

    def remap(self, remaper):
        if self.stop is False:
            if not isinstance(self.selected, list):
                self.selected = [self.selected]
            newselection = []
            for item in self.selected:
                try:
                    newselection.append(remaper(item))
                except:
                    pass
            self.selected = newselection
        return self

    def remember(self, name, value):
        if isinstance(self.selected, list):
            newselection = []
            for item in self.selected:
                item[name] = value
                newselection.append(item)
            self.selected = newselection
        else:
            self.selected[name] = value
        return self

    def unlist(self):
        if isinstance(self.selected, list):
            newitems = []
            for item in self.selected:
                new = {}
                for k, v in item.items():
                    if isinstance(v, list):
                        if len(v) == 1:
                            new[k] = v[0]
                            continue
                        elif not v:
                            new[k] = None
                            continue
                    new[k] = v
                newitems.append(new)
            self.selected = newitems
        else:
            new = {}
            for k, v in self.selected.items():
                if isinstance(v, list):
                    if len(v) == 1:
                        new[k] = v[0]
                        continue
                    elif not v:
                        new[k] = None
                        continue
                new[k] = v
            self.selected = new
        return self
