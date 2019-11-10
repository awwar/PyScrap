from json_mapper.mapper import map_json2
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from parse import BaseParser


class Api(BaseParser):

    def __init__(self, api, setting):
        self.selected = {}
        self.url = api
        self.session = Session()
        self.session.headers.update(setting)
        self.stop = False

    def fetch(f):
        def wrapper(self, *args, **kvargs):
            self.stop = False
            self.selected = {}
            try:
                data = f(self, *args, **kvargs)
                if data.status_code is not 200:
                    self.stop = True
                else:
                    self.selected = json.loads(data.text.encode('utf-8').strip())
            except (ConnectionError, Timeout, TooManyRedirects) as e:
                self.stop = True
            except:
                pass
            return self

        return wrapper

    @fetch
    def fetchapi(self, params):
        return self.session.get(self.url, params=params)

    @fetch
    def postapi(self, params):
        return self.session.post(self.url, params=params)

    def map(self, mapping_config, fun=None, limit=None):
        if self.stop is True:
            return self
        try:
            self.selected = map_json2(mapping_config, self.selected, False, limit)
            if isinstance(self.selected, dict):
                self.selected = self.selected.values()
            if fun is not None:
                self.selected = [fun(select) for select in self.selected]
        except Exception as e:
            self.stop = True
        return self
