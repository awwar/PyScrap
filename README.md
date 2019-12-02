# PyScrap
## Easy to use!
```python
from scrapper import Scrap

baseurl = "https://www.someaddr.io/path/to/page"
settings = {
    'required': [
        'name'
    ]
}

scrapper = Scrap()
result = scrapper.cffetch(settings=settings) \
    .gocs('name', "div.nameclass", lambda a: a.text) \
    .gore('region', r'\"region\"\:\"(.*?)\"', lambda a: a.group(1)) \
    .goxp('builders', '/path/to/builders[count>1]', lambda a: a.text) \
    .gonext(
        baseurl,
        re=r"\"pageNumber\":(\d*?)",
        fun=lambda o: int(o.group(1)) + 1,
        baseaddr=baseurl + '?p={0}'
    )
print(result)
```