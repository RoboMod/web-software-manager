import urllib2
import json
import pickle
import os


def getJSONFromGithub(url):
    # get web cache
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../cache/web.cache"), "r")
    requests = {}
    try:
        requests = pickle.load(f)
    except Exception as e:
        pass

    # create request
    header = {'Accept': 'application/vnd.github.v3+json'}
    if requests.has_key(url):
        header.update({'If-None-Match': requests[url]["etag"]})
    request = urllib2.Request(url, None, header)

    # run request
    try:
        result = urllib2.urlopen(request)
    except urllib2.HTTPError as h:
        # if http code 304 occurs: no new data is available
        if h.code == 304:
            return requests[url]["json"]
        else:
            print "HTTP Error " + str(h.code)
            return {}
    except urllib2.URLError as u:
        print "URL Error (not contact)"
        return {}
    else:
        # if http code 304 occurs: no new data is available
        if result.code == 304:
            return requests[url]["json"]

        # get json data
        data = json.loads(result.read())

        # save url and etag in cache
        requests.update({result.geturl(): {"etag": result.info()["ETag"], "json": data}})
        f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../cache/web.cache"), "w")
        pickle.dump(requests, f, 0)

        # return data
        return data


def getVersionsFromGithub(repo):
    """Returns all versions listet as tags in the given Github repository. repo has to be [owner/repository]"""

    tags = getJSONFromGithub("https://api.github.com/repos/" + repo + "/tags")
    versions = {}

    if tags:
        for tag in tags:
            version = {tag["name"]: {}}
            version[tag["name"]]["url"] = tag["tarball_url"]

    #        commit = getJSONFromGithub(tag["commit"]["url"])
    #        if commit:
    #            version[tag["name"]]["date"] = commit["commit"]["author"]["date"]

            versions.update(version)

    #return sorted(versions, key=lambda v: v["date"])
    return versions


def getArchiveFromGithub(url, name, version):
    # create request
    #url = "https://github.com/" + repo + "/archive/" + version + ".tar.gz"
    request = urllib2.Request(url) #, None, {'Accept': 'application/vnd.github.v3+json'})

    # run request
    try:
        result = urllib2.urlopen(request)
    except urllib2.HTTPError as h:
        print "HTTP Error " + str(h.code)
        return False
    except urllib2.URLError as u:
        print "URL Error (not contact)"
        return False
    else:
        #create dir, if it doesn't exist yet
        if not os.path.isdir("cache/" + name + "/"):
            os.mkdir("cache/" + name + "/")

        output = open("cache/" + name + "/" + version + ".tar.gz", 'w')
        output.write(result.read())
        output.close()
        return True