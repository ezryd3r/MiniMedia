import os
import convert
import config


def main():
    # Open results file in -append mode
    f = open(results_file, 'a')
    for sec in program_list:
        section = sec[0]
        allowed_size = sec[1]
        library = os.path.join(plex_library, section)
        archive = os.path.join(plex_library, 'Archive', section)
        file_list = convert.getfilelist(library, allowed_size, results_file)
        # Future work, figure out wtf this line means (Lambda?)
        # This line makes sure that the largest files are at the top
        list_sorted = sorted(file_list, key=lambda x: x[2])
        max_files = len(list_sorted)
        # If there's more than 3 files in list, just do 3
        if max_files > nConvert:
            max_files = nConvert
        count = 0
        print('Files found = ' + str(max_files))
        while count < max_files:
            item = list_sorted.pop()
            media_file = item[0]
            path = item[1]
            arch = convert.archive_file(media_file, path, archive, library)
            # convert.convert_file(arch, path, hbFormat, handbrake_cli)
            print 'Converted ' + media_file
            f.write(media_file + '\n')
            count = count + 1
    f.close()


if __name__ == "__main__":
    results_file = config.results_file
    program_list = config.program_list
    plex_library = config.plex_library
    nConvert = config.nConvert
    hbFormat = config.hbFormat
    handbrake_cli = config.handbrake_cli
    main()
