# PyScrap
## Easy to use!
```python
from scrappers.CFetch import CFetch

baseurl = "https://www.someaddr.io/path/to/page"
scrapper = CFetch(settings={
    'required': [
        'name'
    ]
})

result = scrapper \
    .gocs('name', "div.nameclass", lambda a: a.text()) \
    .gore('region', r'\"region\"\:\"(.*?)\"', lambda a: a.group(1)) \
    .goxp('builders', '/path/to/builders[count>1]', lambda a: a.text()) \
    .gonext(
        baseurl,
        re=r"\"pageNumber\":(\d*?)",
        fun=lambda o: int(o.group(1)) + 1,
        baseaddr=baseurl + '?p={0}',
        limit=5
    )
print(result)
```