# coding=utf-8
import time

import cfscrape
from lxml import html

from rules.selector import CSSSelection, XPATHSelector, RregularExpressionSelector
from scrappers.parse import BaseParser, rule
from utility.Arguments import GonextArguments, WalkouterArguments


class CFetch(BaseParser):

    def __init__(self, settings=None):
        BaseParser.__init__(self)
        self.cssselectorrule = CSSSelection(settings)
        self.xpathselectorrule = XPATHSelector(settings)
        self.reselectorrule = RregularExpressionSelector(settings)
        self.fetcher = cfscrape.create_scraper()

    def run(self, url):
        self.dom = self.__getdom(url)
        rez = self.__getcontent(self.dom)
        if rez is not None:
            self.selected.append(rez)
        return self.selected

    def gonext(self, **kvargs):
        for href in self.__iterate_url(GonextArguments(kvargs)):
            self.run(href)
        return self.selected

    def walkOuter(self, **kvargs):
        aargs = WalkouterArguments(kvargs)
        for hrefs in self.__iterate_url(aargs):
            dom = self.__getdom(hrefs)
            data = self.__geturl(dom, aargs.are, aargs.axs, aargs.acs, aargs.ahandler, False)
            for href in data:
                self.run(aargs.baseaddr.format(href))
            self.dom = dom
        return self.selected

    @rule
    def gocs(self, name, selector, handler=lambda o: o):
        return self.cssselectorrule.make(name, selector, handler)

    @rule
    def goxs(self, name, selector, handler=lambda o: o):
        return self.xpathselectorrule.make(name, selector, handler)

    @rule
    def gore(self, name, selector, handler=lambda o: o):
        return self.reselectorrule.make(name, selector, handler)

    def __iterate_url(self, args):
        url = args.url
        yield url
        while True:
            if args.limit is not None:
                args.limit -= 1
            try:
                data = self.__geturl(self.dom, args.re, args.xs, args.cs, args.handler)
            except:
                break

            if args.baseaddr is not None:
                href = args.baseaddr.format(data)
            else:
                href = data
            yield href

            if args.limit == 0:
                break
            url = href

    def __forRule(self, dom):
        data = {}
        for instance in self.rules:
            try:
                instance.exequtor.run(data, dom, *instance.args, **instance.kvargs)
            except Exception as e:
                raise Exception('')
        return data

    def __getdom(self, url):
        get = self.fetcher.get(url).content.decode('utf-8')
        dom = html.fromstring(get)

        if (isinstance(dom, list)) and len(dom) > 0:
            dom = dom[0]

        time.sleep(1)
        return dom

    def __getcontent(self, dom):
        content = None

        try:
            content = self.__forRule(dom)
        except:
            pass

        return content

    def __geturl(self, dom, re, xs, cs, handler, limitation=True):
        data = {}
        try:
            if re:
                self.reselectorrule.run(data, dom, '_url', re, handler)
            elif xs:
                self.xpathselectorrule.run(data, dom, '_url', xs, handler)
            elif cs:
                self.cssselectorrule.run(data, dom, '_url', cs, handler)
            else:
                raise Exception
        except Exception as e:
            pass

        data = data.get('_url', [])

        if limitation:
            if (isinstance(data, list)) and len(data) > 0:
                data = data[0]

                data = str(data)

            if not data or data is None:
                raise Exception

        if (isinstance(data, str)) and len(data) < 1:
            raise Exception

        return data
