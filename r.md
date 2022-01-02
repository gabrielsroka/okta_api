a few years ago, when I was first learning Python and looking for http functionality, i found the batteries-included `urllib` -- part of the Python std lib
https://docs.python.org/3/library/urllib.request.html and it said
> The [Requests package](https://requests.readthedocs.io/en/master/) is recommended for a higher-level HTTP client interface.

so i decided to try `requests` instead.

the `requests` page links to a [gist](https://gist.github.com/kennethreitz/973705) 
that makes `urllib` seem very complicated (and `requests` so much easier)
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

so, i learned `requests`, forgot about `urllib` and that was the end of that. or was it?

a few days ago, i was reading about `pprint` and they had this [example](https://docs.python.org/3/library/pprint.html#example) using `urllib` (slightly edited below)
```python
with urllib.request.urlopen('https://pypi.org/pypi/sampleproject/json') as res:
    project = json.load(res)
```

and i thought: "hey, that doesn't look too hard" and wondered if i should give `urllib` a second look. so i did.

i wrote a mini-`requests` lib called `r` using `urllib`. it handles json, gzip and link headers.
it does almost everything i need except for connection-keep-alive (not supported by `urllib`) ~~and some url stuff (coming soon&trade;)~~.
the bulk of it is about 15 LOC. https://github.com/gabrielsroka/okta_api/blob/master/r.py

and here's a small test/demo suite: https://github.com/gabrielsroka/okta_api/blob/master/test_r.py

by contrast `requests` is 7,000-10,000 LOC, and it uses `urllib3` (which is different than `urllib`) which is 20,000-25,000 LOC (http://line-count.herokuapp.com/)

am i saying 15 LOC does everything that 27,000-35,000 LOC does? of course not! or am i?

spending a few hours researching/writing `r` helped me understand and appreciate `requests`.
