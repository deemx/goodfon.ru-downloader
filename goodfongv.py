import urllib.request
import re
import gevent


GOODURL = 'http://www.goodfon.ru/'

def image_download(url):
    pic = urllib.request.urlopen(url)
    img_url = re.findall(r'<a href="(\/download\/.*?\/\d+x\d+)" target.*?>\d+x\d+', str(pic.read()))
    img_dwn = urllib.request.urlopen(GOODURL + img_url[0])
    img = re.findall(r'<a href=\"(http:\/\/img\d\..*?\.jpg)', str(img_dwn.read()))
    img_name = re.findall(r'([\w+-]{0,}\w+\.jpg)$', img[0])
    
    image = urllib.request.urlopen(img[0])
    gevent.sleep(0)
    img_file = open(img_name[0], mode='wb')
    img_file.write(image.read())
    img_file.close()

    
if __name__ == '__main__':
    site = urllib.request.urlopen(GOODURL)
    pattern = re.compile(r"\<div class=\"tabl_td\".+?\<a href\=\"(.+?)\" title\=\".+?\"\>")
    urls = pattern.findall(str(site.read()))
    jobs = [gevent.spawn(image_download(url)) for url in urls]
    gevent.joinall(jobs)
