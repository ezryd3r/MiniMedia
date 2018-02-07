import os

# Test Area Config
plex_library = 'C:\Users\Nick\Documents\GitHub\MiniMedia\TestPlexLibrary'
handbrake_cli = 'C:\Users\Nick\Documents\GitHub\MiniMedia\hb\HandBrakeCLI.exe'  # Handbrake location
hbFormat = ' --preset "Apple 720p30 Surround"'  # Handbrake settings
allowed_movie_size = 1  # GB
allowed_tv_size = 1  # GB
nConvert = 4  # Number files to convert in one go (Stops after this number of conversions)
program_list = [('Movies', allowed_movie_size), ('TV Shows', allowed_tv_size)]
results_file = os.path.join(plex_library, 'Archive', 'conversionresults.txt')
# sqlite3 Database
plexdb = 'plexdb.sqlite'
