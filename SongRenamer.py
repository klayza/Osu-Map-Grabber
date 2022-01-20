import os
import shutil

# This script will retrieve the .mp3 and background image into a contained folder from your osu song folder
# Gets rid of the series of numbers at the start of the .mp3 as well as the osu junk files so you don't have to

# Initialization
while True:
    Destination = input("Enter your destination folder: ")
    if Destination == "df":
        Destination = "D:/Media/Osu! Songs" # Directory the destination will exist in
    elif not os.path.exists(Destination):
        res = input("This path doesn't exist, would you like to create this path anyways? ").upper()
        if "Y" in res:
            os.makedirs(Destination)

    Folder = input("Enter the folder containing your beatmaps: ")
    if Folder == "df":
        Folder = "C:/Users/clayj/AppData/Local/osu!/Songs"     # Directory of unprocessed songs to retrieve(Osu song folder)
        if not os.path.exists(Folder):
            print("Osu folder not found\n")
            continue
    elif not os.path.exists(Folder):
        print("Osu folder not found\n")
        continue
    break

Indicator = Destination + "/#INDICATOR#"   # Control folder: Stores creation time value for comparison


# This terribly written function clears out the junk files that are usually only meant for osu songs
# Walks down path of given path and compares the file with any of the conditional statements for deletion

def osuFileCleanser(startpath):
    removed = 0
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)  # Used for displaying the file tree
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if ".wav" in f:
                os.remove(root + "/" + f)
                removed += 1
            elif ".avi" in f:
                os.remove(root + "/" + f)
                removed += 1
            elif ".db" in f:
                os.remove(root + "/" + f)
                removed += 1
            elif ".flv" in f:
                os.remove(root + "/" + f)
                removed += 1
            elif ".lrc" in f:
                os.remove(root + "/" + f)
                removed += 1
            elif ".mp4" in f:
                os.remove(root + "/" + f)
                removed += 1
            elif ".mpg" in f:
                os.remove(root + "/" + f)
                removed += 1
            elif ".osb" in f:
                os.remove(root + "/" + f)
                removed += 1
            elif ".osu" in f:
                os.remove(root + "/" + f)
                removed += 1
            elif ".wmv" in f:
                os.remove(root + "/" + f)
                removed += 1
            elif ".mp3" in f:
                if os.path.getsize(root + "/" + f) < 500000:
                    os.remove(root + "/" + f)
                    removed += 1
            elif ".jpg" in f:
                if os.path.getsize(root + "/" + f) < 16000:
                    os.remove(root + "/" + f)
                    removed += 1
            elif ".ogg" in f:
                if os.path.getsize(root + "/" + f) < 600000:
                    os.remove(root + "/" + f)
                    removed += 1
            elif ".png" in f:
                if os.path.getsize(root + "/" + f) < 200000:
                    os.remove(root + "/" + f)
                    removed += 1
            else:
                continue
    print("\nFile cleansing complete.\nRemoved:", removed)

# This function gets each folder in the directory of your osu songs and compares it with the indicator folder
# If the folder was created after the indicator folder's date then it is copied to the destination folder

def osuFileGrabber():
    b_count = 0
    s_count = 0
    dl_all = False
    # If this is the first time running and the user has pre-existing songs
    if not os.path.exists(Indicator):
        os.makedirs(Indicator)
        dl_all = True
    for folder in os.listdir(Folder):
        if dl_all:
            shutil.copytree(Folder + "/" + folder, Destination + "/" + folder, dirs_exist_ok=True)  # src, dst
            b_count += 1
            continue
        elif os.path.getctime(Folder + "/" + folder) == os.path.getctime(Indicator):
            s_count += 1
            continue
        elif os.path.getctime(Folder + "/" + folder) < os.path.getctime(Indicator):
            s_count += 1
            continue
        elif int(os.path.getctime(Folder + "/" + folder)) > int(os.path.getctime(Indicator)):
            shutil.copytree(Folder + "/" + folder, Destination + "/" + folder, dirs_exist_ok=True)  # src, dst
            b_count += 1

            # Removes and creates a new indicator folder to make a new creation date

    os.rmdir(Indicator)
    os.mkdir(Indicator)
    print("\nFile retrieval complete.\nSkipped:", s_count, "\nRetrieved:", b_count)

# Rids the pregenerated beatmap code

def ridInitialNumbers(song_folder): # Ex. 839412 Camellia - Diastrophism -> Camellia - Diastrophism
    condition = True
    temp_string = ""
    for char in song_folder:
        if char == " ":
            condition = False
        while condition:
            if char == "1" or "2" or "3" or "4" or "5" or "6" or "7" or "8" or "9":
                break
        else:
            temp_string += char
    return temp_string

# This function

def osuFileRenamer():
    count = 0
    f_count = 0
    song_folders: list = os.listdir(Destination)
    for song_folder in song_folders:
        # Expanding the name to the full path, to ensure that it works regardless of current directory.
        full_song_folder_path: str = os.path.join(Destination, song_folder)
        try:
            mp3_files: list = [entry for entry in os.listdir(full_song_folder_path) if
                               entry.endswith(".mp3") and os.path.isfile(os.path.join(full_song_folder_path, entry))]
        except:
            print("\nFile renaming complete.\nChanged: " + str(count) + "\nFailed: " + str(f_count))
            return Null

        for mp3_file in mp3_files:
            old_path: str = os.path.join(Destination, song_folder, mp3_file)
            new_path: str = os.path.join(Destination, song_folder, ridInitialNumbers(os.path.basename(song_folder)) + ".mp3")
            try:
                os.rename(old_path, new_path)
                count += 1
            except:
                f_count += 1
                continue
    print("\nFile renaming complete.\nChanged: " + str(count) + "\nFailed: " + str(f_count))


def Main():
    osuFileGrabber()
    osuFileCleanser(Destination)
    osuFileRenamer()
    input("\nPress any key to close...")

Main()

