from software import Software


class DokuWiki(Software):
    def __init__(self):
        self.github_repo = "splitbrain/dokuwiki"

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
