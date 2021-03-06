# -*- coding: utf-8 -*-

from module.plugins.internal.Crypter import Crypter

import re


class PastedCo(Crypter):
    __name__    = "PastedCo"
    __type__    = "crypter"
    __version__ = "0.01"

    __pattern__ = r'http://pasted\.co/\w+'

    __description__ = """Pasted.co decrypter plugin"""
    __license__     = "GPLv3"
    __authors__     = [("Frederik Möllers", "fred-public@posteo.de")]


    NAME_PATTERN = r'<title>(?P<N>.+?) - .+</title>'
    NAME_PATTERN = r"'save_paste' href=\"(http://pasted.co/[0-9a-f]+)/info"

    FS_URL_PREFIX = '<pre id=\'thepaste\' class="prettyprint">'
    FS_URL_SUFFIX = '</pre>'

    def decrypt(self, pyfile):
        package = pyfile.package()
        package_name = package.name
        package_folder = package.folder
        html = self.load(pyfile.url, decode = True).splitlines()
        fs_url = None
        FS_URL_RE = re.compile('%s/fullscreen\.php\?hash=[0-9a-f]*' % pyfile.url)
        for line in html:
            match = FS_URL_RE.search(line)
            if match:
                fs_url = match.group()
                break
        if not fs_url:
            raise Exception("Could not find pasted.co fullscreen URL!")
        urls = self.load(fs_url, decode = True)
        urls = urls[urls.find(PastedCo.FS_URL_PREFIX) + len(PastedCo.FS_URL_PREFIX):]
        urls = urls[:urls.find(PastedCo.FS_URL_SUFFIX)].splitlines()
        self.packages.append((package_name, urls, package_folder))
