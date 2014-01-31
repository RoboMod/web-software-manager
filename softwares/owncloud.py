from helpers.files import getInfosFromFile
from helpers.web import *
from helpers.others import *
from software import Software
import os
#import re


class OwnCloud(Software):
    def __init__(self):
        self.github_repo = "owncloud/core"

    def check(self, directory):
        if not os.path.isfile(os.path.join(directory, "index.php")):
            return False

        if not os.path.isfile(os.path.join(directory, "remote.php")):
            return False

        if not os.path.isfile(os.path.join(directory, "public.php")):
            return False

        if not os.path.isfile(os.path.join(directory, "version.php")):
            return False

        if not os.path.isdir(os.path.join(directory, "config")):
            return False

        if not os.path.isfile(os.path.join(directory, "config/config.php")):
            return False

        if None in self.getConfig(directory).values():
            return False

        return True


    def getConfig(self, directory):
        return getInfosFromFile(os.path.join(directory, "config/config.php"),
                ["dbtype", "dbname", "dbuser", "dbpassword", "dbhost", "appstoreurl"],
                '.*\s*=>\s*["\']?([^"\']*)["\']?,')


    def update(self, directory):
        return None


    def download(self, version):
        return None


    def getVersions(self, only_stable=True):
        versions = getVersionsFromGithub(self.github_repo)
        return filter_versions(versions, 'v([\d*\.]*\d).*', 'v[\d*\.]*\d(.*)', only_stable)
