import re


def getInfosFromFile(file, search_strings, regexp_string):
    regexp = re.compile(regexp_string, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    search_results = {}
    # pre fill results
    for string in search_strings:
        search_results[string] = None

    for line in open(file):
        for string in search_results.keys():
            if string in line:
                res = regexp.match(line)
                if res is not None:
                    search_results[string] = res.group(1)

    return search_results
