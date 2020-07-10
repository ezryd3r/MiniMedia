import os
import config
from video import Movie, TVShow
import pickle
from config import logger

class PlexDB:

    def __init__(self, dbpath, plex_path=config.plex_library):
        self.dbpath = dbpath
        self.plex_path = plex_path
        self.data = None
        self.get_lib_data()

    def get_lib_data(self):
        if os.path.isfile(self.dbpath):
            self.data = self.load_db()
            logger.info("Checking for new Movies....")
            self.find_new_files(self.plex_path[0],'Movies')
            logger.info("Checking for new TV Shows....")
            self.find_new_files(self.plex_path[1],'TV Shows')
            self.save_db()
        else:
            logger.info('No database found, creating ' + self.dbpath)
            data = {}
            data['movies'] = []
            data['shows'] = []
            self.data = data
            logger.info("Checking for new Movies....")
            self.find_new_files(self.plex_path[0],'Movies')
            logger.info("Checking for new TV Shows....")
            self.find_new_files(self.plex_path[1],'TV Shows')
            self.save_db()

    def save_db(self):
        pickle.dump( self.data, open(self.dbpath, 'wb' ) )

    def load_db(self):
        data = pickle.load( open(self.dbpath, 'rb' ) )
        return data

    def find_new_files(self, library, type):
        lib_path = library
        for root, __, files in os.walk(lib_path):
            for name in files:
                """ Check this isn't a leftover _old file """
                filename = os.path.join(root, name)
                if "_old" in name:
                    logger.info( "Reverting leftover file " + name)
                    os.rename(filename,filename.replace("_old",""))
                else:
                    if type is 'Movies':
                        self.add_movie(filename)
                    else:
                        self.add_show(filename)

    def add_movie(self, filename):
        movie = Movie(filename)
        if movie.check_is_video and movie.check_size(50000000) and self.check_entry_exists(filename, 'movies'):
            self.data['movies'].append({
                'title': movie.name,
                'year': movie.get_year(),
                'size': movie.size,
                'filename': movie.filename,
                'created': movie.created,
                'converted': 'No'
            })
            logger.info(movie.name + ' added!')

    def add_show(self, filename):
        show = TVShow(filename)
        if show.check_is_video and show.check_size(1000000) and self.check_entry_exists(filename, 'shows'):
            s, e = show.get_episode_data()
            self.data['shows'].append({
                'show': show.name,
                'season': s,
                'episode': e,
                'size': show.size,
                'filename': show.filename,
                'created': show.created,
                'converted': 'No'
            })
            logger.info(show.name + ' added!')

    def list_movies(self):
        nMovies = 0
        total_size = 0
        for m in self.data['movies']:
            print_movie(m)
            nMovies += 1
            size = round(float(m['size']) / 1000000000, 2)
            total_size += size
        print(str(nMovies) + ' Movies found.')
        print('Total Movie library size: ' + '{0:.2f}'.format(round(total_size)) + 'GB')
        print(' ')

    def list_shows(self):
        nShows = 0
        for m in self.data['shows']:
            print_show(m)
            nShows += 1
        print(str(nShows) + ' Episodes found.')
        # print('Total TV Show library size: ' + '{0:.2f}'.format(round(total_size, 2)) + 'GB')
        print(' ')

    def check_entry_exists(self, filename, video_type):
        library = self.data[video_type]
        if not any(filename in row.values() for row in library):
            return True
        else:
            return False

    def clean_plexdb(self):
        for db, lib in self.data.iteritems():
            logger.info("Checking for surplus " + db + "...")
            for f in lib:
                if  not os.path.isfile(f['filename']):
                    logger.info(f['filename'] + " not found!")
                    lib.remove(f)
        self.save_db()


def print_movie(m):
    print('Title: ' + m['title'])
    print('Year: ' + str(m['year']))
    size = round(float(m['size']) / 1000000000, 2)
    print('Size: ' + str(size) + 'GB')
    print('Converted?: ' + m['converted'])
    print('Filename: ' + m['filename'])
    print(' ')


def print_show(show):
    print('Title: ' + show['show'])
    print('Season ' + str(show['season']))
    print('Episode ' + str(show['episode']))
    size = float(show['size']) / 1000000000
    print('Size: ' + str(size) + 'GB')
    print(' ')

def main():
    dbfile = config.plexdb
    Database = PlexDB(dbfile, config.plex_library)
    Database.clean_plexdb()


if __name__ == '__main__':
    main()
