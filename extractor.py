# Clayton Wieberg 6/7/2022
# Manage osu! maps by making copies of each beatmap's song and background image
# AKA SongRenamer V2

from distutils import extension
import os
import shutil


'''
    Flow:

    Goes over each folder in the unprocessed osu! songs folder
    1. Starts with the first folder in unprocessed
    2. Appends the root path of each file within folder to a list
    3. Removes unwanted files from list
    4. Formats list to a dictionary of paths and file sizes
    5. Finds the largest sized file of a song and image
    6. Makes new folder in destination directory
    7. Copies chosen song and image to new directory named as the containing folders title
    8. Continues with next folder

'''


# TODO: Osu adds a (i) to the end of the folder when there is a duplicate song folder, so blacklist these from being copied


unprocessed_folder = "C:/Users/cw1a/AppData/Local/osu!/Songs"
processed_folder = "C:/Users/cw1a/Music/Osu!"
unwanted_files = [".wav", ".avi", ".flv", ".lrc", ".mp4", ".mpg", ".osb", ".osu", ".wmv",]
accepted_song_types = [".mp3", ".ogg"]
accepted_image_types = [".jpg", ".png", ".jpeg"]


def Main():
    copied_folders_count = 0
    skipped_folders_count = 0
    junk_files_count = 0
    folders = os.listdir(unprocessed_folder)
    processed_folders = os.listdir(processed_folder)
    print(f"Starting work on {len(folders)} folders\n{'-'*40}")
    
    # Iteratively copies the entire folder to the destination

    for folder in folders:
        index = str(folders.index(folder) + 1)
        new_name = stripID(folder)

        # When a song has already been processed
        if new_name.upper() in str(processed_folders).upper():
            #print(f"{index} | Already exists")
            continue
        source = f"{unprocessed_folder}/{folder}"
        full_path_files = []
        error = False   # Used if a folder doesn't have a song

        # Walks through the folder and grabs it's contents

        for root, dirs, files in os.walk(source):
            
            # Iterates through each file within the folder
            
            for file in files:
                current_file = root + "/" + file
                
                # Skips the unwanted file types
                
                for type in unwanted_files:
                    if type in current_file:
                        junk_files_count += 1
                        break
                    # Only executes when the list is at the end
                    elif unwanted_files.index(type) == len(unwanted_files) - 1:
                        full_path_files.append(current_file)


            # Groups the potential songs and background images by lists
                
        songs = [x for x in full_path_files if ".MP3" in x.upper() or ".OGG" in x.upper()]
        images = [x for x in full_path_files if ".JPG" in x.upper() or ".PNG" in x.upper() or ".JPEG" in x.upper()]
            
        # When a folder doesn't have a song
        if len(songs) == 0:
            skipped_folders_count += 1
            print(f"{index} | Missing song, skipping: {new_name} ")
            continue

        # Determines the right song (based on file size)
        
        songs_and_sizes = dict.fromkeys(songs)
        for song in songs:
            songs_and_sizes[song] = os.path.getsize(current_file)
        sorted = list(songs_and_sizes.values())
        sorted.sort()
        chosen_song = list(songs_and_sizes.keys())[list(songs_and_sizes.values()).index(sorted[-1])]
        
        # Determines the right image (based on file size)
        if len(images) != 0:
            images_and_sizes = dict.fromkeys(images)
            for image in images:
                images_and_sizes[image] = os.path.getsize(image)
            sorted = list(images_and_sizes.values())
            sorted.sort()
            chosen_image = list(images_and_sizes.keys())[list(images_and_sizes.values()).index(sorted[-1])]

        # Creates the new folder and copies files

        song_extension = os.path.splitext(os.path.basename(chosen_song))[1] 
        image_extension = os.path.splitext(os.path.basename(chosen_image))[1]
        new_dir = f"{processed_folder}/{new_name}"
        os.makedirs(new_dir, exist_ok=True)
        shutil.copyfile(chosen_song, f"{new_dir}/{new_name + song_extension}")   # Song
        if len(images) != 0:
            shutil.copyfile(chosen_image, f"{new_dir}/{new_name + image_extension}")    # Image

        print(f"{index} | Finished {new_name}")
        copied_folders_count += 1
    print(f"\nDone\nCopied {copied_folders_count} folders\nAvoided {junk_files_count} files\nSkipped {skipped_folders_count} folders")


# Removes the numbers in the beginning of the folder name
def stripID(folder):
    condition = True
    temp_string = ""
    for char in folder:
        if char == " ":
            condition = False
        while condition:
            if char in "0123456789":
                break
            else:
                break
        else:
            temp_string += char
    return temp_string.strip()




Main()