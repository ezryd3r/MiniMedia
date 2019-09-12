
from plexdb import PlexDB, print_movie
from video import Movie
import config
import logging
import logging.config

#logging.config.fileConfig('logging.conf')
# create logger
#logger = logging.getLogger('simpleExample')
# 'application' code
#logger.debug('debug message')
#logger.info('info message')
#logger.warn('warn message')
#logger.error('error message')
#logger.critical('critical message')
# TODO get convert list for TV Show
# TODO Implement logging before deploying to server.
# TODO Update database with movies already converted


def get_convert_list(plexdb, allowed_size, max_convert):
    count = 1
    conv_list = []
    file_dict = plexdb.data['movies']
    for row in file_dict:
        size = row['size']
        conv = row['converted']
        if check_size(size, allowed_size * 1000000000) and check_converted(conv) and count <= max_convert:
            conv_list.append((row['filename'], size))
            count += 1
            print("Movie to be added:")
            print_movie(row)
# TODO Sort By Largest
    return conv_list


def check_size(size, allowed):
    if size > allowed:
        return True


def check_converted(c):
    if c == 'No':
        return True


def main():
    dbfile = config.plexdb
    db = PlexDB(dbfile, config.plex_library)
    conv_list = get_convert_list(db, config.allowed_movie_size, 5)
    for m in conv_list:
        mov = Movie(m[0])
        print(mov.name)


if __name__ == "__main__":
    main()
