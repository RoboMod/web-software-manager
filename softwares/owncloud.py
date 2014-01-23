import helpers
from software import Software

class OwnCloud(Software):
  def __init__(self):
    pass
  
  def check(self, dir):
    return None
  
  def getConfig(self, dir):
    return None
  
  def update(self, dir):
    return None
  
  def download(self, version):
    return None
  
  def getVersions(self):
    helpers.getVersionsFromGithub("owncloud/core")
    return None
