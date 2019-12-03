# coding=utf-8
import time

import cfscrape
from lxml import html

from rules.selector import CSSSelection, XPATHSelector, RregularExpressionSelector
from scrappers.parse import BaseParser, rule


class CFetch(BaseParser):

    def __init__(self, settings=None):
        BaseParser.__init__(self)
        self.cssselectorrule = CSSSelection(settings)
        self.xpathselectorrule = XPATHSelector(settings)
        self.reselectorrule = RregularExpressionSelector(settings)
        self.fetcher = cfscrape.create_scraper()

    def run(self, url):
        rez = self.__getcontent(url)
        if rez is not None:
            self.selected.append(rez)
        return self.selected

    def gonext(self, url, cs=None, xs=None, re=None, fun=None, baseaddr=None, limit=None):
        self.selected = []
        for href in self.__iterate_url(url, cs, xs, re, fun, baseaddr, limit):
            self.run(href)
        return self.selected

    def walkOuter(self, url, cs=None, xs=None, re=None, fun=None, baseaddr=None, limit=None):
        pass

    @rule
    def gocs(self, name, selector, handler=lambda o: o):
        return self.cssselectorrule.make(name, selector, handler)

    @rule
    def goxs(self, name, selector, handler=lambda o: o):
        return self.xpathselectorrule.make(name, selector, handler)

    @rule
    def gore(self, name, selector, handler=lambda o: o):
        return self.reselectorrule.make(name, selector, handler)

    def __iterate_url(self, url, cs=None, xs=None, re=None, handler=None, baseaddr=None, limit=None):
        yield url
        while True:
            if limit is not None:
                limit -= 1
            try:
                if re is not None:
                    data = self.reselectorrule.run(self.dom, '_url', re, handler)
                elif xs is not None:
                    data = self.xpathselectorrule.run(self.dom, '_url', xs, handler)
                elif cs is not None:
                    data = self.cssselectorrule.run(self.dom, '_url', cs, handler)
                else:
                    break
            except:
                data = None

            data = data.get('_url')
                
            if (isinstance(data, list)) and len(data) > 0:
                data = data[0]

            if not data or data is None:
                break

            data = str(data)

            if (isinstance(data, str)) and len(data) < 1:
                break

            if baseaddr is not None:
                href = baseaddr.format(data)
            else:
                href = data
            yield href

            time.sleep(1)

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
        get = self.fetcher.get(url).content.decode('utf-8')
        self.dom = html.fromstring(get)

        if (isinstance(self.dom, list)) and len(self.dom) > 0:
            self.dom = self.dom[0]

        content = None

        try:
            content = self.__forRule()
        except:
            pass

        return content
