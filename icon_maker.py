import json
import os
import pathlib
import re
import urllib
import urllib.parse as up
from urllib import request
import requests
from PIL import Image
from PIL import ImageDraw

MOVIE_DB_TOKEN = "c3fabad95853f3161cf8a45b254ac7da"


# Error function
def err(txt):
    print(f'ERROR: {txt}')
    exit()


# download pic poster from tmdb
def down_pic(url):
    try:
        res = requests.get("https://image.tmdb.org/t/p/original" + url)
        assert res.content is not None

        return res.content
    except:
        err("Can't get image from tmdb")


# Add corner to pic
def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


# Save pic in poster temp and save ico in wanted folder
def make_ico(id, folder, pic_url):
    main_folder = str(pathlib.Path(__file__).parent.absolute())

    if not os.path.exists(f"{main_folder}/poster/"):
        os.mkdir(f"{main_folder}/poster/")

    if not os.path.exists(f"{main_folder}/poster/{id}.jpg"):
        urllib.request.urlretrieve(pic_url, f"{main_folder}/poster/{id}.jpg")

    if not os.path.exists(folder + '/cover.ico'):
        size = (339, 461)
        im = Image.open(main_folder + "/poster/" + id + '.jpg')
        back = Image.open(main_folder + "/Cover.png")
        ov = Image.open(main_folder + "/ov.png")
        im.thumbnail(size, Image.ANTIALIAS)
        im = add_corners(im, 11)
        im.paste(ov, (0, 0), ov)
        back.paste(im, (59, 24), im)
        back.save(folder + '/cover.ico')


# Get imdb id from google result
def get_imdb_id(movie_name):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
            'Content-Type': 'text/html',
        }
        response = requests.get(f"https://www.imdb.com/find?q={up.quote(movie_name)}&ref_=nv_sr_sm", headers=headers)
        res = re.findall(r'\/title\/([^"]+)\/', response.text)[0]

        assert res is not None
        return res
    except:
        err("Can't get imdb id from google result")


# Get poster path from movie db
def get_poster_path(imdb_id, is_movie):
    try:
        url = f"http://api.themoviedb.org/3/find/{imdb_id}?api_key={MOVIE_DB_TOKEN}&external_source=imdb_id"
        response = requests.get(url)
        if is_movie:
            return json.loads(response.text)['movie_results'][0]['poster_path']
        else:
            return json.loads(response.text)['tv_results'][0]['poster_path']
    except:
        err("Can't find poster path from movie db")


def config_icon(path):
    if os.path.exists(f"{path}/desktop.ini"):
        raise Exception("desktop.ini exists")
    ds = open(f"{path}/desktop.txt", "w")
    ds.write(f"""[.ShellClassInfo]
    IconResource={path}/cover.ico,0""")
    ds.close()
    os.rename(f"{path}/desktop.txt", f"{path}/desktop.ini")
    os.system(f'attrib +s "{path}"')
    os.system(f'attrib +h "{path}/desktop.ini"')
    os.system(f'attrib +h "{path}/cover.ico"')


def refresh_icons():
    os.system(r"c:\ie4uinit.exe -ClearIconCache")
    os.system(r"c:\ie4uinit.exe -show")


def get_pic_ins(movie_name):
    try:
        s = movie_name
        s = s.lower().strip()
        s = f"{s[0]}/{s}"
        s = re.sub(r"\s+", "_", s.lower().strip())
        res = requests.get(f"https://v2.sg.media-imdb.com/suggestion/{s}.json")
        return res.json()['d'][0]['i']['imageUrl'], res.json()['d'][0]['id']
    except:
        err("Can't get pic instantly from imdb")
