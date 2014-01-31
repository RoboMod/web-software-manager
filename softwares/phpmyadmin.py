from software import Software
import helpers
import os


class phpMyAdmin(Software):
    def __init__(self):
        self.github_repo = "phpmyadmin/phpmyadmin"

    def check(self, directory):
        return False

    def getConfig(self, directory):
        return None

    def update(self, directory):
        return None

    def download(self, version):
        return None

    def getVersions(self, only_stable=True):
        versions = helpers.getVersionsFromGithub(self.github_repo)
        return helpers.filter_versions(versions, 'RELEASE_([\d*_]*\d).*', 'RELEASE_[\d*_]*\d(.*)' , only_stable)
