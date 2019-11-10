from lxml import html
import cfscrape
import re
from rules.selector import CSSSelection, XPATHSelector, RregularExpressionSelector
from parse import BaseParser, rule


class CFfetch(BaseParser):

    def __init__(self, settings=None):
        BaseParser.__init__(self)
        self.selected = {}
        self.cssselector = CSSSelection(settings)
        self.xpathselector = XPATHSelector(settings)
        self.reselector = RregularExpressionSelector(settings)
        self.scraper = cfscrape.create_scraper()
        self.dom = None
        self.url = None
        self.cut = None

    def run(self, url):
        self.url = url
        self.cut = cut
        self.dom = self.__getcontent(self.url)
        selected = {}
        for instance in self.rules:
            try:
                executor = instance.exequtor
                selected.update(executor.run(self.dom, *instance.args, **instance.kvargs))
            except Exception as e:
                self.selected = None
                return
        self.selected = [selected]
        return self.selected

    def walk(self, url, cs=None, xs=None, re=None, fun=None, baseaddr=None, limit=None):
        self.url = url
        selected = []
        for href in self.iterate_url(self.url, cs, xs, re, fun, baseaddr, limit):
            self.dom = self.__getcontent(href)
            data = {}
            for instance in self.rules:
                try:
                    executor = instance.exequtor
                    data.update(executor.run(self.dom, *instance.args, **instance.kvargs))
                except Exception as e:
                    self.selected = None
                    return
            selected.append(data)
        return selected

    def iterate_url(self, url, cs=None, xs=None, re=None, handler=None, baseaddr=None, limit=None):
        yield url
        while True:
            if limit is not None:
                limit -= 1
            try:
                if re is not None:
                    data = self.reselector.run(self.dom, '_', re, handler)
                elif xs is not None:
                    data = self.xpathselector.run(self.dom, '_', xs, handler)
                elif cs is not None:
                    data = self.cssselector.run(self.dom, '_', cs, handler)
                else:
                    break
            except:
                data = None

            data = data.get('_')

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
            yield href
            if limit == 0:
                break
            url = href

    def __getcontent(self, url):
        self.stop = False
        self.selected = {}
        get = self.scraper.get(url).content
        # get = urllib2.urlopen(url).read()
        self.dom = html.fromstring(get)

        if (isinstance(self.dom, list)) and len(self.dom) > 0:
            self.dom = self.dom[0]

        if self.cut is not None:
            self.dom = self.dom.cssselect(self.cut)
            if self.dom:
                self.dom = self.dom[0]
        return self.dom

    @rule
    def gocs(self, name, selector, handler=None):
        return self.cssselector.make(name, selector, handler)

    @rule
    def goxs(self, name, selector, handler=None):
        return self.xpathselector.make(name, selector, handler)

    @rule
    def gore(self, name, selector, handler=None):
        return self.reselector.make(name, selector, handler)
