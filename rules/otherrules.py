from baserule import *


class RememberRule(RuleExecutor):

    def __init__(self):
        pass

    def run(self, data, dom, *args, **kvargs):
        data.update({args[0]: args[1]})


class RemapRule(RuleExecutor):

    def __init__(self):
        pass

    def run(self, data, dom, *args, **kvargs):
        remap = args[0]
        data = remap(data)
