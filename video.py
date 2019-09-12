import os
import re
import config
import shutil
import ntpath


class Video:

    def __init__(self, filename=None):
        self.filename = filename
        self.name = ntpath.basename(filename)
        self.root = self.filename.replace(self.name, '')
        #self.filename = os.path.join(self.root, self.name)
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

    def archive_video(self):
        # Create Archive folder by removing p_path from mov_file string
        folder_path = self.filename.replace(config.plex_library, '')
        # Source file
        src = self.filename
        # Destination File
        arch_path = os.path.join(config.plex_library, 'Archive')
        dst = os.path.join(arch_path, folder_path)
        dst_folder = dst.strip(self.name)
        # Create Destination folder if required
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)
            print 'Created folder ' + dst_folder
        # Move file to archive
        shutil.move(src, dst)
        print 'File ' + self.name + ' Moved to Archive'
        return dst

    def get_extension(self):
        _, file_extension = os.path.splitext(self.filename)
        return file_extension

    def convert(self):
        # Remove File extension and change to .mp4
        # filename, file_extension = os.path.splitext(path)
        # dst = filename + '.mp4'
        # print 'Source ' + src
        # print 'Destination ' + dst
        # # Run Handbrake
        # subprocess.call([config.handbrake_cli, "-i", src, "-o", dst, hb_format])
        # print 'Conversion of ' + src + ' was successful!'
        # time.sleep(5)
        print(self.name + ' has been converted')


class Movie(Video):

    def __init__(self, filename):
        Video.__init__(self, filename)

    def get_year(self):
        num_list = re.findall('\d{4}', self.name)
        for n in num_list:
            if 1900 <= int(n) <= 2050:
                return int(n)


class TVShow(Video):

    def __init__(self, filename):
        Video.__init__(self, filename)

    def get_episode_data(self):
        s = re.findall(r"S(\d{1,2})", self.name)
        e = re.findall(r"E(\d{1,2})", self.name)
        return s[0], e[0]

    def check_new_show(self, c):
        c.execute("SELECT id FROM shows WHERE Title = ?", (self.name,))
        data = c.fetchall()
        if len(data) == 0:
            return True
        else:
            return False
