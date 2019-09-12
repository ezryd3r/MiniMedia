import json
import os
import config
from video import Movie, TVShow
import logging
import logging.config


class PlexDB:

    def __init__(self, dbpath, plex_path=config.plex_library):
        self.dbpath = dbpath
        self.plex_path = plex_path
        self.data = None
        self.get_lib_data()

    def get_lib_data(self):
        if os.path.isfile(self.dbpath):
            logging.info('Found Database, loading library data...')
            self.data = self.load_json()
        else:
            print('No database found, creating ' + self.dbpath)
            data = {}
            data['movies'] = []
            data['shows'] = []
            self.data = data
            self.find_new_files('Movies')
            # self.find_new_files('TV Shows')
            self.save_json()

    def save_json(self):
        with open(self.dbpath, 'w') as outfile:
            json.dump(self.data, outfile)

    def load_json(self):
        with open(self.dbpath) as json_file:
            return json.load(json_file)

    def find_new_files(self, library):
        movie_path = os.path.join(self.plex_path, library)
        for root, dirs, files in os.walk(movie_path):
            for name in files:
                filename = os.path.join(root, name)
                if library is 'Movies':
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
            print(movie.name + ' added!')

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
            print(show.name + ' added!')

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
        total_size = 0
        for m in self.data['shows']:
            print('Title: ' + m['show'])
            print('Season ' + str(m['season']))
            print('Episode ' + str(m['episode']))
            size = float(m['size']) / 1000000000
            total_size += size
            print('Size: ' + str(size) + 'GB')
            print(' ')
            nShows += 1
        print(str(nShows) + ' Episodes found.')
        print('Total TV Show library size: ' + '{0:.2f}'.format(round(total_size, 2)) + 'GB')
        print(' ')

    def check_entry_exists(self, filename, video_type):
        library = self.data[video_type]
        if not any(filename in row.values() for row in library):
            return True
        else:
            return False


# TODO Create print_show
def print_movie(m):
    print('Title: ' + m['title'])
    print('Year: ' + str(m['year']))
    size = round(float(m['size']) / 1000000000, 2)
    print('Size: ' + str(size) + 'GB')
    print('Converted?: ' + m['converted'])
    print('Filename: ' + m['filename'])
    print(' ')


def main():
    dbfile = 'Plex_json.txt'
    Database = PlexDB(dbfile, config.plex_library)
    Database.find_new_files('Movies')
    Database.find_new_files('TV Shows')
    # Database.list_movies()
    # Database.list_shows()


if __name__ == '__main__':
    main()
