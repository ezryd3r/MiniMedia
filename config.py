import os

# Test Area Config
plex_library = 'C:\Users\Nick\Documents\Coding Working Area\Plex Media Library'
handbrake_cli = 'C:\Users\Nick\Documents\GitHub\MiniMedia\hb\HandBrakeCLI.exe'  # Handbrake location
hbFormat = ' --preset "Apple 720p30 Surround"'  # Handbrake settings
allowed_movie_size = 1  # GB
allowed_tv_size = 0.01  # GB
nConvert = 3  # Number files to convert in one go (Stops after this number of conversions)
program_list = [('Movies', allowed_movie_size), ('TV Shows', allowed_tv_size)]
results_file = os.path.join(plex_library, 'Archive', 'conversionresults.txt')
# sqlite3 Database
plexdb ='Plex_json.txt'
video_extensions = ['.mp4', '.avi', '.mkv', '.m4v']
