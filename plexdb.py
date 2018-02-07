import sqlite3
import config
import convert
import os
import re


def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    conn.text_factory = str
    c = conn.cursor()
    return c, conn


def movie_table(c):
        c.execute("CREATE TABLE IF NOT EXISTS movies(id integer PRIMARY KEY, Title text, year integer, size integer)")


# Get's list of files that meet the conversion criteria
def getmovielist(plex_path, c):
    data = []
    for root, dirs, files in os.walk(plex_path):
        for name in files:
            videoextensions = ['.mp4', '.avi', '.mkv', '.m4v']
            filename, size, created = convert.getfiledata(root, name)
            ch1 = convert.checkvideo(name, videoextensions)
            ch2 = convert.checksize(size, 1)
            if ch1 and ch2:
                year = get_year(name)
                data = [name, year, size]
                c.execute('''INSERT INTO movies(Title,Year,Size) VALUES(?,?,?)''', data)
    return data


def get_year(name):
    num_list = re.findall('\d+', name)
    for n in num_list:
        if 1900 <= int(n) <= 2050:
            year = int(n)
            break
    else:
        year = 0000
    return year


def main():
        db_file = config.plexdb
        c, conn = create_connection(db_file)
        movie_table(c)
        getmovielist(config.plex_library, c)
        # Print the results
        print('Printing Movie Table')
        c.execute('''SELECT * FROM movies''')
        for row in c:
            print(row)
        conn.commit()
        conn.close()


if __name__ == '__main__':
        main()
