from software import Software
import helpers
import os


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
        return helpers.getInfosFromFile(os.path.join(directory, "config/config.php"),
                ["dbtype", "dbname", "dbuser", "dbpassword", "dbhost", "appstoreurl"],
                '.*\s*=>\s*["\']?([^"\']*)["\']?,')


    def update(self, directory):
        return None


    def download(self, version):
        versions = self.getVersions(False)

        if versions:
            if versions.has_key(version):
                return helpers.getArchiveFromGithub(versions[version]['url'], self.__class__.__name__, version)
            else:
                print "unknown version (" + version + ")!"
        else:
            print "no versions found!"

        return False



    def getVersions(self, only_stable=True):
        versions = helpers.getVersionsFromGithub(self.github_repo)
        return helpers.filter_versions(versions, 'v([\d*\.]*\d).*', 'v[\d*\.]*\d(.*)', only_stable)
