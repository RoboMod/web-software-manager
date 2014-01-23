import urllib2
import json
import pickle

def getJSONFromGithub(url):
  # get web cache
  f = open("cache/web.cache", "r")
  requests = []
  try:
    requests = pickle.load(f)
  except Exception as e:
    pass
  
  # create request
  request = urllib2.Request(url, None, {'Accept': 'application/vnd.github.v3+json'})
  
  # run request
  try:
    result = urllib2.urlopen(request)
  except urllib2.HTTPError as h:
    print "http error"
    print h.code
    return None
  except urrlib2.URLError as u:
    print "url error"
    return None
  else:
    # get json data
    data = json.loads(result.read())
    
    # save url and etag in cache
    requests += {"url" : result.geturl(), "etag" : result.info()["ETag"]}
    f = open("cache/web.cache", "w")
    pickle.dump(requests, f, 0)
    
    # return data
    return data

def getVersionsFromGithub(repo):
  """Returns all versions listet as tags in the given Github repository. repo has to be [owner/repository]"""
  
  tags = getJSONFromGithub("https://api.github.com/repos/"+repo+"/tags")
  
  if tags != None :
    versions = []
    for tag in tags:
      version = {}
      version["version"] = tag["name"]
      version["url"] = tag["tarball_url"]
      
      commit = getJSONFromGithub(tag["commit"]["url"])
      if commit != None :
	version_data["date"] = commit["commit"]["author"]["date"]
	
      versions.append(version)
    
    print versions
    
def getArchiveFromGithub(software, repo, version):
  # create request
  url = "https://github.com/"+repo+"/archive/"+version+".tar.gz"
  request = urllib2.Request(url, None, {'Accept': 'application/vnd.github.v3+json'})
  
  # run request
  try:
    result = urllib2.urlopen(request)
  except urllib2.HTTPError as h:
    print "http error"
    print h.code
    return None
  except urrlib2.URLError as u:
    print "url error"
    return None
  else:
    output = open("cache"+software+url.split('/')[-1],'w')
    output.write(result.read())
    output.close()