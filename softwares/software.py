class Software(object):

    github_repo = None

    def __init__(self):
        pass

    #def getVersion(self, directory):
    #  return None

    #def getDBName(self, directory):
    #  return None

    #def getDBUser(self, directory):
    #  return None

    #def getDBPassword(self, directory):
    #  return None

    def check(self, directory):
        return False

    def getConfig(self, directory):
        return None

    def update(self, directory):
        return None

    def download(self, version):
        return None

    def getVersions(self):
        return {}

    #def getStableVersion(self):
    #  return None