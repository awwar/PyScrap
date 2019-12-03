class GonextArguments:
    def __init__(self, kvargs):
        self.url = kvargs.get('url')

        if self.url is None:
            raise Exception('Attribute "url" must be set!')

        self.re = kvargs.get('re', False)
        self.cs = kvargs.get('cs', False)
        self.xs = kvargs.get('xs', False)

        if not (self.re or self.cs or self.xs):
            raise Exception('Filter query "re" or "xs" or "cs" must be set!')

        self.handler = kvargs.get('handler')
        self.baseaddr = kvargs.get('baseaddr')

        if self.baseaddr is None:
            raise Exception('Attribute "baseaddr" must be set!')

        self.limit = kvargs.get('limit')


class WalkouterArguments(GonextArguments):
    def __init__(self, kvargs):
        GonextArguments.__init__(self, kvargs)
        self.tile = kvargs.get('tile')

        if self.tile is None:
            raise Exception('Attribute "tile" must be set!')

        self.are = self.tile.get('re', False)
        self.acs = self.tile.get('cs', False)
        self.axs = self.tile.get('xs', False)

        if not (self.are or self.acs or self.axs):
            raise Exception('Filter "tile" query "re" or "xs" or "cs" must be set!')

        self.ahandler = self.tile.get('handler', False)
