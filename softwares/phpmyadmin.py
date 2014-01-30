from software import Software


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

    def getVersions(self):
        return {}
