moved to https://github.com/gabrielsroka/r

a few years ago, when I was first learning Python and looking for http functionality, i found the batteries-included `urllib` -- part of the Python std lib
https://docs.python.org/3/library/urllib.request.html and it said
> The [Requests package](https://requests.readthedocs.io/en/master/) is recommended for a higher-level HTTP client interface.

so i decided to try `requests` instead.

the `requests` page links to a [gist](https://gist.github.com/kennethreitz/973705) that makes `urllib` seem very complicated (and `requests` so much easier)
```python
import urllib2

gh_url = 'https://api.github.com'

req = urllib2.Request(gh_url)

password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_manager.add_password(None, gh_url, 'user', 'pass')

auth_manager = urllib2.HTTPBasicAuthHandler(password_manager)
opener = urllib2.build_opener(auth_manager)

urllib2.install_opener(opener)

handler = urllib2.urlopen(req)
```

so i learned `requests`, forgot about `urllib`, and that was the end of that. or was it?

a few days ago, i was reading about `pprint` and there was an [example](https://docs.python.org/3/library/pprint.html#example) using `urllib` (slightly edited)
```python
with urlopen('https://pypi.org/pypi/sampleproject/json') as res:
    project = json.load(res)
```

and i thought: "hey, that doesn't look too hard" and wondered if i should give `urllib` a second look. so i did.

i wrote a mini `requests` lib called `r` using `urllib`. it handles json, gzip and link headers.
it does almost everything i need except for connection-keep-alive (which is not supported by `urllib`) ~~and some url stuff (coming soon&trade;)~~.

[source](https://github.com/gabrielsroka/okta_api/blob/master/r.py)

and here's a small [test/demo suite](https://github.com/gabrielsroka/okta_api/blob/master/test_r.py)

the bulk of `r` is about 15 LOC. by contrast `requests` is 4,000 LOC, and it uses `urllib3` (which is different than `urllib`) and other libraries as well (http://line-count.herokuapp.com/)

am i saying 15 LOC does everything that 4,000 LOC does? of course not!

spending a few hours learning `urllib` and other libraries, and writing `r` helped me understand and appreciate `requests`.
