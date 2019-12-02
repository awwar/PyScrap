# coding=utf-8


class Rule:
    def __init__(self, exequtor, *args, **kvargs):
        self.exequtor = exequtor
        self.args = args
        self.kvargs = kvargs


class RuleExecutor:
    def make(self, *args, **kvargs):
        return Rule(self, *args, **kvargs)

    def run(self, data, dom, *args, **kvargs):
        pass
