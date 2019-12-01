# coding=utf-8
from Scrappers.CFfetch import CFfetch


class Scrap:

    def cffetch(self, settings=None):
        return CFfetch(settings)

    def fetch(self, url, cut=None, settings=None):
        pass

    def walk(self, url, cut=None, cs=None, xs=None, re=None, fun=None, baseaddr=None, limit=None):
        yield url
        while True:
            self.walkselected.append(self.selected)
            if limit is not None:
                limit -= 1
            self.fetch(url, cut)
            if re is not None:
                self.gore('_walk', re, fun=fun)
            elif xs is not None:
                self.goxs('_walk', xs, fun=fun)
            elif cs is not None:
                self.gocs('_walk', cs, fun=fun)
            else:
                raise Exception('')

            data = self.selected.get('_walk')
            if not data or data is None:
                break
            if len(data) > 0:
                data = data[0]

            if not data or not isinstance(data, str) or len(data) < 1:
                break

            if baseaddr is not None:
                href = baseaddr % data
            else:
                href = data
            self.selected = {}
            yield href
            if limit == 0:
                break
            url = href