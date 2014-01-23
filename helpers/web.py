import urllib2
import json
import pickle

def getVersionsFromGithub(repo):
  """Returns all versions listet as tags in the given Github repository. repo has to be [owner/repository]"""
  
  f = open("helpers/web.cache", "r")
  try:
    requests = pickle.load(f)
    print requests
  
  request = urllib2.Request("https://api.github.com/repos/"+repo+"/tags", None, {'Accept': 'application/vnd.github.v3+json'})
  
  try:
    result = urllib2.urlopen(request)
  except urllib2.HTTPError as h:
    #print h.code
    return False
  except urrlib2.URLError as u:
    return False
  else:
    data = json.loads(result.read())
    requests.append({"etag" : result.info["ETag"]})
    versions = []
    for version in data:
      version_data = {}
      version_data["version"] = version["name"]
      version_data["url"] = version["tarball_url"]
      
      request = urllib2.Request(version["commit"]["url"], None, {'Accept': 'application/vnd.github.v3+json'})
      try:
	result = urllib2.urlopen(request)
      except urllib2.HTTPError as h:
	pass
      except urrlib2.URLError as u:
	pass
      else:
	commit_data = json.loads(result.read())
	version_data["date"] = commit_data["commit"]["author"]["date"]
	
      versions.append(version_data)
    
    f = open("helpers/web.cache", "w")
    pickle.dump(requests, f, 0)
    
    print versions