# coding=utf-8
import time

import cfscrape
from lxml import html

from rules.selector import CSSSelection, XPATHSelector, RregularExpressionSelector
from scrappers.parse import BaseParser, rule


class CFfetch(BaseParser):

    def __init__(self, settings=None):
        BaseParser.__init__(self)
        self.cssselector = CSSSelection(settings)
        self.xpathselector = XPATHSelector(settings)
        self.reselector = RregularExpressionSelector(settings)
        self.scraper = cfscrape.create_scraper()
        self.dom = None

    def run(self, url):
        self.selected.append(self.__getcontent(url))
        return self.selected

    def gonext(self, url, cs=None, xs=None, re=None, fun=None, baseaddr=None, limit=None):
        self.selected = []
        for href in self.__iterate_url(url, cs, xs, re, fun, baseaddr, limit):
            self.selected.append(self.__getcontent(href))
            time.sleep(1)
        return self.selected

    def walkOuter(self, url, cs=None, xs=None, re=None, fun=None, baseaddr=None, limit=None):
        pass

    @rule
    def gocs(self, name, selector, handler=None):
        return self.cssselector.make(name, selector, handler)

    @rule
    def goxs(self, name, selector, handler=None):
        return self.xpathselector.make(name, selector, handler)

    @rule
    def gore(self, name, selector, handler=None):
        return self.reselector.make(name, selector, handler)

    def __iterate_url(self, url, cs=None, xs=None, re=None, handler=None, baseaddr=None, limit=None):
        yield url
        while True:
            if limit is not None:
                limit -= 1
            try:
                if re is not None:
                    data = self.reselector.run(self.dom, '_url', re, handler)
                elif xs is not None:
                    data = self.xpathselector.run(self.dom, '_url', xs, handler)
                elif cs is not None:
                    data = self.cssselector.run(self.dom, '_url', cs, handler)
                else:
                    break
            except:
                data = None

            data = data.get('_url')

            if not data or data is None:
                break
            if len(data) > 0:
                data = data[0]

            if not data or data is None:
                break

            if (isinstance(data, str)) and len(data) < 1:
                break

            data = str(data)

            if baseaddr is not None:
                href = baseaddr.format(data)
            else:
                href = data
            yield href
            if limit == 0:
                break
            url = href

    def __forRule(self):
        data = {}
        for instance in self.rules:
            try:
                instance.exequtor.run(data, self.dom, *instance.args, **instance.kvargs)
            except Exception as e:
                raise Exception('')
        return data

    def __getcontent(self, url):
        self.stop = False
        get = self.scraper.get(url).content.decode('utf-8')
        self.dom = html.fromstring(get)

        if (isinstance(self.dom, list)) and len(self.dom) > 0:
            self.dom = self.dom[0]

        content = []

        try:
            content = self.__forRule()
        except:
            pass

        return content
