class Element:

    def __init__(self, lxmldata):
        self.__lxmldata = lxmldata
        self.tag = lxmldata.tag
        self.label = lxmldata.label
        self.href = lxmldata.attrib.get('href')
        self.id = lxmldata.attrib.get('id')
        self.classname = lxmldata.attrib.get('class')
        self.name = lxmldata.attrib.get('name')
        self.placeholder = lxmldata.attrib.get('placeholder')
        self.src = lxmldata.attrib.get('src')
        self.style = lxmldata.attrib.get('style')
        self.value = lxmldata.attrib.get('value')

    def data(self, key):
        return self.__lxmldata.attrib.get("data-%s" % key)

    def custom(self, key):
        return self.__lxmldata.attrib.get(key)

    def text(self, isstrip=True, encode='utf-8'):
        text = self.__lxmldata.text
        if not text or text is None:
            text = self.__lxmldata.text_content()
        if not text or text is None:
            return None
        if isstrip:
            text = text.strip('\n\t ')
        return text.encode(encode)
