# Import modules
import os
import time
import subprocess
from Queue import Queue
import shutil


# Create list of files to be converted
def create_list(p_path, allowed_size):
    # Getting filename and path as i've no idea what i'm doing
    name_results = Queue(maxsize=0)
    filename_results = Queue(maxsize=0)
    check_size = allowed_size * 1000000000
    # List all files
    print "List all files over " + str(allowed_size) + "GB in " + p_path
    print "==================" + "=" * len(p_path)
    for root, dirs, files in os.walk(p_path):
        for name in files:
            filename = os.path.join(root, name)
            size = os.stat(filename).st_size
            # Find files that are larger than ALLOWED_SIZE
            if size > check_size:
                print name
                name_results.put(name)
                filename_results.put(filename)
    print 'List creation completed'
    return name_results, filename_results


# Move file to Archive folder
def archive_file(mov_file, mov_path, arch_path, p_path):
    # Create Archive folder by removing p_path from mov_file string
    folder_path = mov_path.replace(p_path, '')
    # Source file
    src = mov_path
    # Destination File
    dst = arch_path + folder_path
    dst_folder = dst.strip(mov_file)
    # Create Destination folder if required
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
        print 'Created folder ' + dst_folder
    # Move file to archive
    shutil.move(src, dst)
    print 'File ' + mov_file + ' Moved to Archive'
    return dst


# Function to convert files using HandBrakeCLI
def convert_file(src, path, hb_format, handbrake_cli):
    # Remove File extension and change to .mp4
    filename, file_extension = os.path.splitext(path)
    dst = filename + '.mp4'
    print 'Source ' + src
    print 'Destination ' + dst
    # Run Handbrake
    subprocess.call([handbrake_cli, "-i", src, "-o", dst, hb_format])
    print 'Conversion of ' + src + ' was successful!'
    time.sleep(5)
    return


def getfiledata(root, name):
        filename = os.path.join(root, name)
        size = os.stat(filename).st_size
        created = os.path.getmtime(filename)
        return filename, size, created


# Checks file is actually a video
def checkvideo(name, video_extensions):
    if any(x in name for x in video_extensions):
        return True


# Checks if file is older than 3 months
def checkage(created):
    now = time.time()
    if now - created > 1:  # (3 * 30 * 24 * 60 * 60):
        return True


# Checks if file is bigger than allowed file size
def checksize(size, allowed_size):
    check = allowed_size * 1000000000
    if size > check:
        return True


# Get's list of files that meet the conversion criteria
def getfilelist(plex_path, allowed_size, results_file):
    file_list = []
    for root, dirs, files in os.walk(plex_path):
        for name in files:
            videoextensions = ['.mp4', '.avi', '.mkv', '.m4v']
            filename, size, created = getfiledata(root, name)
            ch1 = checkvideo(name, videoextensions)
            ch2 = checkage(created)
            ch3 = checksize(size, allowed_size)
            ch4 = checkarch(results_file, name)
            if ch1 and ch2 and ch3 and ch4:
                data = [name, filename, size]
                file_list.append(data)
    return file_list


# Checks that video does not appear in the converted videos file
def checkarch(media_file, video):
    z = open(media_file, 'r')
    converted = z.readlines()
    converted = [x.strip() for x in converted]
    if video not in converted:
        return True
