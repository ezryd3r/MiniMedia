# config_example.py

######################################################################################################
# Rename this file config.py (remove the _example) once you have filled in all sections.
######################################################################################################

# MiniMedia Configuration

#=====================================================================================================
# plex_library[0]		Movie folder path
# plex_library[1]		TV Show Folder path
# handbrake_cli			HandbrakeCli.exe location
# hb_format 			Handbrake settings
# allowed_movie_size	Allowed Movie Size in GB
# allowed_tv_size		Allow TV Show Size in GB
# nConvert_movie		Number of movie files to convert in one go (Stops after this number of conversions)
# nConvert_show 		Number of tv show files to convert in one go (Stops after this number of conversions)
# plexdb				Name of Your json database, default='Plex_json.txt'
# video_extensions		List of wanted video extentions default=['.mp4', '.avi', '.mkv', '.m4v']
#=====================================================================================================
plex_library = ["path\to\movie\folder",'\path\to\show\Folder']
handbrake_cli = 'path\to\\HandbrakeCLI\HandBrakeCLI.exe'
hb_format = ' --preset "Fast 1080p30" --all-audio --audio-lang-list eng -E copy:ac3  --all-subtitles'
allowed_movie_size = 5
allowed_tv_size = 0.5
nConvert_movie = 0
nConvert_show = 2  
plexdb = 'Plex_json.txt'
video_extensions = ['.mp4', '.avi', '.mkv', '.m4v']
