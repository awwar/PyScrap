from baserule import *


class RememberRule(RuleExecutor):

    def __init__(self):
        RuleExecutor.__init__(self)

    def run(self, data, dom, *args, **kvargs):
        data.update({args[0]: args[1]})


class RemapRule(RuleExecutor):

    def __init__(self):
        RuleExecutor.__init__(self)

    def run(self, data, dom, *args, **kvargs):
        remap = args[0]
        data = remap(data)
