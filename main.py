import os

from icon_maker import get_pic_ins, make_ico, config_icon

if __name__ == '__main__':
    """Set movie icon"""
    # Validation
    path = input("movie path: ")
    movie_name = os.path.basename(os.path.normpath(path)).strip()
    try:
        url, movie_id = get_pic_ins(movie_name)
        make_ico(movie_id, path, url)
        config_icon(path)

    except Exception as e:
        print(e)
