from cloudscraper import create_scraper
from lxml import html, etree
from subprocess import run, PIPE
from shutil import which
import random
import json
import time
import os


JSONNET = True
NODEJS = True
if not which("node"):
    NODEJS = False
    try:
        import _jsonnet
    except:
        JSONNET = False
if not NODEJS and not JSONNET:
    raise ImportError("js object decoder is required (node.js or jsonnet)")


mirrors = [
    ["https", "lijianm.in"],
    ["https", "xgoogle.xyz"],
    # # ["http", "google.lyz810.com"],
    ["https", "goo.gle.workers.dev"],
    ["https", "googlehnzyc.azurewebsites.net"],
    # ["https", "g20.i-research.edu.eu.org"],
    # ["http", "google.1qi777.com"],
]
TBM = {
    "All": "",
    "Applications": "tbm=app",
    "Blogs": "tbm=blg",
    "Books": "tbm=bks",
    "Discussions": "tbm=dsc",
    "Images": "tbm=isch",
    "News": "tbm=nws",
    "Patents": "tbm=pts",
    "Places": "tbm=plcs",
    "Recipes": "tbm=rcp",
    "Shopping": "tbm=shop",
    "Videos": "tbm=vid",
}
search_url = "https://google.com/search?q={}"


def s():
    s = create_scraper()
    s.headers.update({
        "accept-language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,ru;q=0.6,zh-CN;q=0.5",
    })
    return s


def random_mirror():
    # return mirrors[0]
    # return mirrors[1]
    # return mirrors[2] #
    # return mirrors[3]
    # return mirrors[4]
    # return mirrors[5] #
    # return mirrors[6]
    return random.SystemRandom().choice(mirrors)


def transform(url):
    proto, domain = random_mirror()
    url = url.split("/")
    url[0] = proto+":"
    url[2] = domain
    print("/".join(url))
    return "/".join(url)


def get(url, ss={}):
    url = transform(url)
    d = url.split("/")[2]
    if d not in ss:
        ss[d] = s()
    return ss[d].get(url)


def get_raw(url):
    return get(url).content


def post(url, data, ss={}):
    url = transform(url)
    d = url.split("/")[2]
    if d not in ss:
        ss[d] = s()
    return ss[d].post(url, data=data)


def post_raw(url, data):
    return post(url, data=data).content


def search(kw, cat="All", page=1, raw=True):
    if cat not in TBM:
        raise KeyError(cat)
    url = search_url.format(kw)
    cat = TBM[cat]
    if cat:
        url += "&{}".format(cat)
    if raw:
        return get_raw(url)
    else:
        return get(url)


def search_all(kw, page=1, raw=True):
    return search(kw, cat="All", page=page, raw=raw)


def search_images(kw, page=1, raw=True):
    return search(kw, cat="Images", page=page, raw=raw)


def parse_images(raw):
    r = html.fromstring(raw.decode())
    rs = [_ for _ in r.xpath("//script[contains(text(), 'AF_initDataCallback')]/text()")]
    if rs:
        r = max(rs, key=len)
        if NODEJS:
            open("tmp.js", "wb").write(("console.log(JSON.stringify("+str(r)[20:-2]+"));").encode())
            r = run("node tmp.js", stderr=PIPE, stdout=PIPE).stdout.decode()
            os.remove("tmp.js")
        elif JSONNET:
            r = _jsonnet.evaluate_snippet("snippet", str(r)[20:-2])
        r = json.loads(r)
        return r["data"][56][1][0][0][1][0]
    else:
        r = [etree.tostring(_, method="html") for _ in r.xpath("//*[@data-ou]")]
        if not r:
            raise ValueError("raw is malformed, try to search and parse again")
        return r


def process_images(parsed):
    r = []
    if isinstance(parsed[0], bytes):
        for _ in parsed:
            _ = html.fromstring(_.decode())
            r.append([
                _.xpath("//div/@data-ru")[0],
                _.xpath("//div/@data-ou")[0],
            ])
    else:
        for i, _ in enumerate(parsed):
            _ = list(_[0][0].values())[0]
            url = img = None
            imgs = []
            urls = []
            if not _[1]:
                continue
            for __ in _[1]:
                if isinstance(__, list):
                    imgs.append(__)
                elif isinstance(__, dict):
                    for ___ in __.values():
                        for ____ in ___:
                            if isinstance(____, str) and ____.startswith("http"):
                                urls.append(____)
            url = urls[0]
            img = imgs[-1][0]
            r.append([
                url,
                img
            ])
    return r


def get_images(**kwargs):
    while True:
        try:
            return process_images(parse_images(search_images(**kwargs)))
        except:
            import traceback
            traceback.print_exc()
            time.sleep(5)


def search_videos(kw, page=1, raw=True):
    return search(kw, cat="Videos", page=page, raw=raw)


def search_news(kw, page=1, raw=True):
    return search(kw, cat="News", page=page, raw=raw)


if __name__ == "__main__":
    # url = "http://google.lyz810.com/search?q=%E7%A7%8B%E8%91%89%E5%8E%9F%E5%86%A5%E9%80%94%E6%88%B0%E7%88%AD&newwindow=1&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjCibvd95H7AhXFm1YBHXWGAPEQ_AUoAXoECAIQAw&biw=1918&bih=1009"
    # print(get_raw(url))
    # print(search_all("秋葉原冥途戰爭"))
    # print(search_images("秋葉原冥途戰爭"))
    # print(parse_images(search_images("秋葉原冥途戰爭")))
    # print(process_images(parse_images(search_images("秋葉原冥途戰爭"))))
    print(get_images(kw="秋葉原冥途戰爭"))

