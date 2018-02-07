import os
import re
import config


class Video:

    def __init__(self, root, name):
        self.root = root
        self.name = name
        self.filename = os.path.join(self.root, self.name)
        self.created = os.path.getmtime(self.filename)
        self.size = os.stat(self.filename).st_size

    def check_size(self, check_size):
        if self.size > check_size:
            return True
        else:
            return False

    def check_is_video(self):
        if any(x in self.name for x in config.video_extensions):
            return True


class Movie(Video):

    def __init__(self, root, name,):
        Video.__init__(self, root, name)

    def get_year(self):
        num_list = re.findall('\d+', self.name)
        for n in num_list:
            if 1900 <= int(n) <= 2050:
                return int(n)

    def add_new_movie(self, c):
        data = [self.name, self.get_year(), self.size, "No", self.filename]
        c.execute('''INSERT INTO movies(Title,Year,Size,Converted,Path) VALUES(?,?,?,?,?)''', data)

    def check_new_movie(self, c):
        c.execute("SELECT id FROM movies WHERE Title = ?", (self.name,))
        data = c.fetchall()
        if len(data) == 0:
            print('There is no movie named %s' % self.name)
            return True
        else:
            print('There is a movie named %s' % self.name)
            return False


