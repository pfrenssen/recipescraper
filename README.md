Recipescraper
=============

Returns a list of recipes for the site "Dagelijkse kost".


Requirements
------------

* [Pipenv](https://github.com/pypa/pipenv)
* [Scrapy](https://scrapy.org)


Installation
------------

```
$ pipenv install
```


Usage
-----

```
$ ./venv/bin/scrapy crawl dagelijksekost -o output.json
```

A list of recipes will be saved in `output.json`.
