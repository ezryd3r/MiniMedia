import os

# Test Area Config
plex_library = []  # path to media library [string]
handbrake_cli = []  # path to location of HandBrakeCLI.exe [string]
hbFormat = ' --preset "Apple 720p30 Surround"'  # Handbrake settings
allowed_movie_size = 1  # GB
allowed_tv_size = 1  # GB
nConvert = 4  # Number files to convert in one go (Stops after this number of conversions)
program_list = [('Movies', allowed_movie_size), ('TV Shows', allowed_tv_size)]
results_file = os.path.join(plex_library, 'Archive', 'conversionresults.txt')
# sqlite3 Database
plexdb = 'plexdb.sqlite'
