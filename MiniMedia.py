#!/usr/bin/env python

from plexdb import PlexDB, print_movie, print_show
import config
from video import Movie, TVShow
from config import logger


def get_convert_list_movies(plexdb, allowed_size, max_convert):
    count = 1
    conv_list = []
    for row in plexdb.data['movies']:
        size = row['size']
        conv = row['converted']
        if check_size(size, allowed_size * 1000000000) and check_converted(conv):
            if count >= max_convert:
                return conv_list
            else:
                conv_list.append((row['filename'], size))
                count += 1
                logger.info("Movie to be converted:" + row['title'])
    return conv_list

def get_convert_list_shows(plexdb, allowed_size, max_convert):
    count = 1
    conv_list = []
    for row in plexdb.data['shows']:
        size = row['size']
        conv = row['converted']
        if check_size(size, allowed_size * 1000000000) and check_converted(conv):
            if count <= max_convert:
                conv_list.append((row['filename'], size))
                count += 1
                logger.info("Show to be converted:" + row['show'])
            else:
                return conv_list
    return conv_list


def check_size(size, allowed):
    if size > allowed:
        return True


def check_converted(c):
    if c == 'No':
        return True

def convert_movies(plexdb,file_list):
    for f in file_list:
        filename = f[0]
        mov = Movie(filename)
        success = mov.convert()
        if success:
            for fdb in plexdb.data['movies']:
                if fdb['filename'] == filename:
                    fdb['converted'] = 'Yes'
                    logger.info(filename + ' converted status has been changed to Yes.')
                    plexdb.save_db
                    return

def convert_shows(plexdb,file_list):
    for f in file_list:
        filename = f[0]
        show = TVShow(filename)
        success = show.convert()
        if success:
            for fdb in plexdb.data['shows']:
                if fdb['filename'] == filename:
                    fdb['converted'] = 'Yes'
                    logger.info(filename + ' has been changed to converted')
                    plexdb.save_db()
                    return



def main():
    logger.info("MiniMedia Started...")
    dbfile = config.plexdb
    db = PlexDB(dbfile, config.plex_library)
    db.clean_plexdb()
    conv_list_movies = get_convert_list_movies(db, config.allowed_movie_size, config.nConvert_movie)
    conv_list_shows = get_convert_list_shows(db, config.allowed_tv_size, config.nConvert_show)
    convert_movies(db,conv_list_movies)
    convert_shows(db,conv_list_shows)


if __name__ == "__main__":
    main()
