"""Main entry point for the Canto Subtitle Cleaner module."""

import sys
import os
import traceback
from datetime import datetime
from canto_subtitle_cleaner.srt import srt_to_list, list_to_srt, timecode as srt_timecode
from canto_subtitle_cleaner.clean import clean_subtitle
from canto_subtitle_cleaner.format import adjust_subtitle_breaks

PACKAGE_NAME = 'canto_subtitle_cleaner'
DEBUG_MODE = False  # Set to True for debugging output
OUTPUT_PREFIX = "output_"  # Default prefix added to the output filename
ADD_OFFSET = None

# Take a list of (timecode, subtitle text), clean up all the text, and return it
def clean_subtitle_list(subtitle_list, add_offset=None, add_duration=None):
    new_subtitle_list = []

    for timecode, text in subtitle_list:
        if not isinstance(timecode, srt_timecode):
            raise TypeError("Expected timecode to be of type srt.timecode")

        original_time_start = timecode.start
        block_cleaned_text = clean_subtitle(text).strip()

        if DEBUG_MODE:
            nl = "\n"
            t = "\t"
            replaced_text = text.replace('\n', '\\n')
            replaced_block_text = block_cleaned_text.replace('\n', '\\n')

            print(f"  {original_time_start}: {t}{replaced_text} {nl}→ {timecode.start}: {t}{replaced_block_text}")

        # Skip block if cleaned text is empty
        if not block_cleaned_text:
            continue
                                
        # new_subtitle_list.append((timecode, '\n'.join([block_cleaned_text])))
        new_subtitle_list.append((timecode, block_cleaned_text))

    adjust_subtitle_breaks(new_subtitle_list)

    for timecode, text in subtitle_list:
        if add_offset:
            timecode.add_offset(add_offset)

        if add_duration:
            timecode.add_duration(add_duration)

    return new_subtitle_list

# Clean up subtitles in an input SRT file, then output with a prefix added on the filename
def process_file(input_file, output_directory="", output_prefix="", add_offset=None, add_duration=None):
    try:
        # Derive the output file name
        output_file = f"{output_directory}\\{output_prefix}{os.path.basename(input_file)}"
        
        subtitle_list = srt_to_list(input_file)
        print("Got the input file srt list. Cleaning...")

        subtitle_list = clean_subtitle_list(subtitle_list, add_offset, add_duration)

        with_offset_str = ""
        if add_offset:
            with_offset_str = f" with offset {add_offset.time()}"

        print(f"Cleaned subtitles from the list{with_offset_str}. Outputting to file...")

        list_to_srt(subtitle_list, output_file)
        print(f"File complete. Processed SRT saved to {output_file}.")

    except Exception as e:
        print(f"Error cleaning SRT file {input_file}: {e}")
        traceback.print_exc(file=sys.stdout)
        quit()

# Run process_file on all the SRT files in a directory
def process_directory(input_directory, output_directory="", output_prefix="", add_offset=None, add_duration=None):
    try:
        # List all .srt files in the directory
        srt_files = [f for f in os.listdir(input_directory) if f.endswith('.srt')]

        if not srt_files:
            print(f"No .srt files found in directory: {input_directory}")
            return

        # Process each file
        for srt_file in srt_files:
            full_path = os.path.join(input_directory, srt_file)
            process_file(full_path, output_directory, output_prefix, add_offset, add_duration)

    except Exception as e:
        print(f"An error occurred while processing the directory: {e}")

    return

def print_usage():
    print(f"usage: python -m {PACKAGE_NAME} [<input_file> | -d <input_directory>] [-o <output_directory> | -p <output_prefix>] [--add_offset HH:MM:SS] [--debug]")
    return

######################################## MAIN SECTION #########################################
# Quit the script
def quit():
    #os.system("pause")
    sys.exit(1)

def main():
    global DEBUG_MODE, OUTPUT_PREFIX
    output_directory = ""
    add_offset = None
    add_duration = None

    # Check if there are arguments 
    if len(sys.argv) < 2:
        print(f"Error: No arguments provided. Please add arguments to the command.")
        print_usage()
        quit()

    # Enable debug mode if --debug flag is present
    if "--help" in sys.argv or "-h" in sys.argv or "-?" in sys.argv:
        print_usage()
        quit()

    # Enable debug mode if --debug flag is present
    if "--debug" in sys.argv:
        DEBUG_MODE = True

    # -p argument for output file name prefix
    if "-p" in sys.argv:
        prefix_index = sys.argv.index("-p")
        if prefix_index + 1 < len(sys.argv):
            OUTPUT_PREFIX = sys.argv[prefix_index + 1]
        else:
            print("Error: Missing value for -p argument.")
            print_usage()
            quit()

    # --add_offset
    if "--add_offset" in sys.argv:
        prefix_index = sys.argv.index("--add_offset")
        if prefix_index + 1 < len(sys.argv):
            try:
                add_offset = datetime.strptime(sys.argv[prefix_index + 1], "%H:%M:%S,%f")
            except ValueError:
                print("Error: Invalid time format for --add_offset. Use HH:MM:SS,ms.")
                print_usage()
                quit()
        else:
            print("Error: Missing value for --add_offset argument.")
            print_usage()
            quit()

    # --add_duration
    if "--add_duration" in sys.argv:
        prefix_index = sys.argv.index("--add_duration")
        if prefix_index + 1 < len(sys.argv):
            try:
                add_duration = datetime.strptime(sys.argv[prefix_index + 1], "%H:%M:%S,%f")
            except ValueError:
                print("Error: Invalid time format for --add_duration. Use HH:MM:SS,ms.")
                print_usage()
                quit()
        else:
            print("Error: Missing value for --add_duration argument.")
            print_usage()
            quit()

    # Sanitize and validate input paths
    def validate_path(path):
        if not os.path.exists(path):
            print(f"Error: The path '{path}' does not exist.")
            quit()
        return os.path.abspath(path)
    
    # Process -od output directory argument
    if "-o" in sys.argv:
        prefix_index = sys.argv.index("-o")
        if prefix_index + 1 < len(sys.argv):
            output_directory = validate_path(sys.argv[prefix_index + 1])
        else:
            print("Error: Missing value for -o argument. Please add an output directory.")
            print_usage()
            quit()

    # -d argument for directory of input SRT files
    if sys.argv[1] == "-d":
        if len(sys.argv) < 3:
            print("Error: Missing value for -d argument. Please add an input directory.")
            print_usage()
            quit()
        input_directory = validate_path(sys.argv[2])
        process_directory(input_directory, output_directory, OUTPUT_PREFIX, add_offset, add_duration)
    else:
        input_file = validate_path(sys.argv[1])
        process_file(input_file, output_directory, OUTPUT_PREFIX, add_offset, add_duration)

if __name__ == "__main__":
    main()