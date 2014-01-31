from software import Software
import helpers
import os

class MediaWiki(Software):
    def __init__(self):
        self.github_repo = "wikimedia/mediawiki-core"

    def check(self, directory):
        if not os.path.isfile(os.path.join(directory, "index.php")):
            return False

        if not os.path.isfile(os.path.join(directory, "load.php")):
            return False

        if not os.path.isfile(os.path.join(directory, "api.php")):
            return False

        if not os.path.isfile(os.path.join(directory, "img_auth.php")):
            return False

        if not os.path.isfile(os.path.join(directory, "LocalSettings.php")):
            return False

        if None in self.getConfig(directory).values():
            return False

        return True

    def getConfig(self, directory):
        return helpers.getInfosFromFile(os.path.join(directory, "LocalSettings.php"),
                ["dbtype", "dbname", "dbuser", "dbpassword", "dbserver"],
                '.*\s*=\s*["\']?([^"\']*)["\']?,')

    def update(self, directory):
        return None

    def download(self, version):
        return None

    def getVersions(self, only_stable=True):
        versions = helpers.getVersionsFromGithub(self.github_repo)
        return helpers.filter_versions(versions, '[^\d]*([\d*\.]*\d).*', '[^\d]*[\d*\.]*\d(.*)', only_stable)
