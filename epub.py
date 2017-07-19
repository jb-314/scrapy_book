# -*- coding:utf-8 -*-

'''
epub epub文件对象
'''

import zipfile, os, uuid, datetime

class Epub:
    def __init__(self,filename=None):
        if filename:
            self.epub_name = '%s.epub' % filename
            self.filename = filename
        else:
            path = os.path.basename(os.getcwd())
            self.epub_name = '%s.epub' % path
            self.filename = path
        self.uid = uuid.uuid1()
        self.date = datetime.datetime.now()
        self.epub = zipfile.ZipFile(self.epub_name, 'w')

        self.create_mimetype()
        self.create_container()
        self.create_stylesheet()
        self.create_cover()

    def create_mimetype(self):
        self.epub.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)

    def create_container(self):
        container_info = '''<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n\t<rootfiles>\n\t\t<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n\t</rootfiles>\n</container>'''
        self.epub.writestr('META-INF/container.xml',container_info, compress_type=zipfile.ZIP_STORED)

    def create_stylesheet(self):
        css_info = '''body {\n\tfont-family: sans-serif;\n}\nh1, h2, h3, h4 {\n\tfont-family: serif;\n\tcolor: red;\n}'''
        self.epub.writestr('OEBPS/stylesheet.css',css_info,compress_type=zipfile.ZIP_STORED)

    def create_content(self, lists, creator='epub', language='zh'):
        content_info='''<?xml version="1.0" encoding="UTF-8" ?>\n<package xmlns="http://www.idpf.org/2007/opf" version="2.0">\n\t<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">\n\t\t<dc:title>%(title)s</dc:title>\n\t\t<dc:creator opf:role="aut">%(creator)s</dc:creator>\n\t\t<dc:language>%(language)s</dc:language>\n\t\t<dc:identifier opf:scheme="UUID">%(uid)s </dc:identifier>\n\t\t<dc:date>%(date)s</dc:date>\n\t</metadata>\n\t<manifest>\n\t\t<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>\n\t\t<item href="toc.html" id="toc" media-type="application/xhtml+xml"/>\n\t\t%(manifest)s\n\t</manifest>\n\t<spine toc="ncx">\n\t\t<itemref idref="toc"/>\n\t\t%(spine)s\n\t</spine>\n</package>\n'''
        manifest = ''
        spine = ''
        for l in lists:
            id = l.split('&')[0]
            manifest += '<item id="%s" href="%s" media-type="application/xhtml+xml"/>\n\t\t' % (id, id+'.html')
            spine += '<itemref idref="%s"/>\n\t\t' % (id)
        self.epub.writestr('OEBPS/content.opf',content_info % {
                                    'title': self.epub_name.replace('.epub',''),
                                    'creator': creator,
                                    'language': language,
                                    'uid': self.uid,
                                    'date': self.date,
                                    'manifest': manifest,
                                    'spine': spine,},
                                    compress_type=zipfile.ZIP_STORED)

    def create_ncx(self,lists):
        ncx_info = '''<?xml version='1.0' encoding='utf-8'?>\n<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n\t<head>\n\t\t<meta name="dtb:uid" content="%(uid)s"/>\n\t\t<meta name="dtb:depth" content="1"/>\n\t\t<meta name="dtb:totalPageCount" content="%(total_page)s"/>\n\t\t<meta name="dtb:maxPageNumber" content="%(max_page)s"/>\n\t</head>\n\t<docTitle>\n\t\t<text>%(title)s</text>\n\t</docTitle>\n\t<navMap>\n\t\t%(nav_point)s\n\t</navMap>\n</ncx>'''
        nav_point = ''
        for l in lists:
            id = l.split('&')[0]
            chapter = l.split('&')[1]
            nav_point += '<navPoint id="%(id)s" playOrder="%(id)s">\n\t\t\t<navLabel><text>%(chapter)s</text></navLabel>\n\t\t\t<content src="%(src)s"/></navPoint>\n\t\t' % {
            'id': id,
            'chapter': chapter,
            'src': id + '.html'
            }
        self.epub.writestr('OEBPS/toc.ncx',ncx_info % {
            'uid': self.uid,
            'total_page': len(lists),
            'max_page': len(lists),
            'title': self.epub_name.replace('.epub',''),
            'nav_point': nav_point,},
            compress_type=zipfile.ZIP_STORED)

    def create_chapter(self, filename, file):
        self.epub.writestr('OEBPS/'+filename+'.html', file)

    def create_cover(self):
        _html = '''<?xml version='1.0' encoding='utf-8'?>\n<html xmlns="http://www.w3.org/1999/xhtml">\n\t<head>\n\t\t<mate charset="utf-8">\n\t\t<title>Hello World: My First EPUB</title>\n\t\t<link type="text/css" rel="stylesheet" media="all" href="stylesheet.css" />\n\t</head>\n\t<body>\n\t\t<h1>%s</h1>\n\t</body>\n</html>\n'''
        self.epub.writestr('OEBPS/toc.html', _html % self.epub_name.replace('.epub',''))


    def create_close(self):
        self.epub.close()


if __name__=='__main__':
    e = Epub()
    e.create_content('text','demo','sony')
    e.create_close()
