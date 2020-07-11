import os
import re
import config
import shutil
import ntpath
import time
from subprocess import call
import logging

logger = logging.getLogger(__name__)

class Video:

    def __init__(self, filename=None):
        self.filename = filename
        self.name = ntpath.basename(filename)
        self.root = self.filename.replace(self.name, '')
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

    def get_extension(self):
        _, file_extension = os.path.splitext(self.filename)
        return file_extension

    def convert(self):
        # Remove File extension and change to .mp4
        name, ext = os.path.splitext(self.filename)
        dst = name + '.mp4'
        # Append original file with _old
        src = self.rename_file(name, ext)
        logger.info('Source ' + src)
        logger.info('Destination ' + dst)
        # Run Handbrake
        hb_str = config.handbrake_cli + ' -i "' + src + '" -o "' + dst + '" ' + config.hb_format
        call(hb_str, shell=True)
        successful = self.check_conversion(src,dst)
        if successful:
            os.remove(src)
            logger.info('Conversion of ' + src + ' was successful!')
            return True
        else:
            logger.info("New file is larger than previous, removing new file")
            os.rename(src,self.filename)
            os.remove(dst)
            return False


    def rename_file(self, name, ext):
        new_filename = name + "_old" + ext
        os.rename(self.filename,new_filename)
        logger.info("File: " + self.filename + " Renamed: " +  new_filename)
        return new_filename       

    def check_conversion(self, src, dst):
        original_size = os.stat(src).st_size
        new_size = os.stat(dst).st_size
        # TODO: Split these issues so that if conversion fails you don't set it as converted in the db
        if original_size > new_size and new_size > original_size * 0.1:
            return True


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
