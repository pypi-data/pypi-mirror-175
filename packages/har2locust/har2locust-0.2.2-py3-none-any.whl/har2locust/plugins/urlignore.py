from har2locust.plugin import entriesprocessor
import re
import pathlib


@entriesprocessor
def process(entries):
    urlignore_file = pathlib.Path(".urlignore")
    url_filters = []
    if urlignore_file.is_file():
        with open(urlignore_file) as f:
            url_filters = f.readlines()
            url_filters = [line.rstrip() for line in url_filters]

    entries[:] = [e for e in entries if not any(re.search(r, e["request"]["url"]) for r in url_filters)]
