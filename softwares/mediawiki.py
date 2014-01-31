from software import Software
from helpers.others import *
from helpers.web import *

class MediaWiki(Software):
    def __init__(self):
        self.github_repo = "wikimedia/mediawiki-core"

    def check(self, directory):
        return False

    def getConfig(self, directory):
        return None

    def update(self, directory):
        return None

    def download(self, version):
        return None

    def getVersions(self, only_stable=True):
        versions = getVersionsFromGithub(self.github_repo)
        return filter_versions(versions, '[^\d]*([\d*\.]*\d).*', '[^\d]*[\d*\.]*\d(.*)', only_stable)
