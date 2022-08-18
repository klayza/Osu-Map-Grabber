# Given .m3u8 playlist file and directory of music titles
import shutil
import eyed3
import os

'''
    Flow:

    1. Asks user for a path for m3u file
    2. Appends titles in m3u file to list
    3. Walks through directory of music
    4. Looks for matches in titles
    5. Determines if the favorite song exists from either the filename or ID3 metadata
    5. Copies folder or either single mp3 to output

'''

music_dir = "C:/Users/cw1a/Music"
destination = "C:/Users/cw1a/Music/Favorites"
m3upath = r"Favorites.m3u8"

def m3uTitles(path):
    titles = []
    with open(path, "r+", encoding="utf-8") as f:
        for line in f.readlines():
            if "#EXTINF" in line:
                for i in range(len(line)):
                    if line[i] == ",":
                        titles.append(line[i + 1:].strip())
                        break
    return titles


def getTitle(path):
    audio = eyed3.load(path)
    if audio == None:
        return None
    else: 
        try:
            return audio.tag.title.strip()
        except AttributeError:
            return None


def Main():
    # 1. Asks user for a path for m3u file
    # while True:
    #     m3upath = input("Enter path to m3u file: ")
    #     if not os.path.exists(m3upath):
    #         print("Path not found, try again")
    #         continue
    #     break

    # 2. Appends titles in m3u file to list
    titles = m3uTitles(m3upath)
    unfound = titles
    conflict = {}
    found = []

    print(f"Starting search for {len(titles)} songs\n{'-'*30}")

    # 3. Walks through directory of music and scans for matches
    folders = os.listdir(music_dir)
    for folder in folders:
        if folder == "Favorites": continue
        for root, dirs, files in os.walk(f"{music_dir}/{folder}"):
            for file in files:
                match = False
                current_file = f"{root}/{file}"

                if "JDM" in file:
                    pass

                # Skips non-music files
                if ".mp3" not in file and ".ogg" not in file and ".wav" not in file:
                    continue
                
                title = getTitle(current_file)
                
                # 4. Looks for matches in titles
                for _title in titles:
                    # When the filename is the exact same as a favorite song
                    if _title == file[:-4]:
                        match = True
                        break
                    # When a favorite song title is the same as a song filename
                    if _title in file[:-4]:
                        if _title in list(conflict.keys()):
                            conflict[_title].append(current_file)
                        else:
                            conflict[_title] = [current_file]
                    # elif title not in titles:
                    #     continue
                
                # When a file has an id3 title 
                # Checks if it is among the favorite songs
                if title != None and not match:
                    for _title in titles:
                        if title == _title:
                            match = True
                            break
                # When a file can't find an md3 title 
                elif match:
                    title = _title

                # 5. Copies folder or either single mp3 to output
                if match:
                    contents = os.listdir(root)

                    # When there is a single song in a folder
                    if len(contents) <= 2 and title not in found:
                        shutil.copytree(root, f"{destination}/{title}", dirs_exist_ok=True)
                        print(f"Copied folder | {title}")
                        found.append(title)
                        unfound.remove(title)

                    # When there is many songs in the same folder, so only copies one file
                    elif len(contents) > 2 and title not in found:
                        if not os.path.exists(f"{destination}/{file}"):
                            shutil.copy(current_file, f"{destination}/{file}")
                            print(f"Copied file | {title}")
                            found.append(title)
                            unfound.remove(title)
    
    # Results
    print("\nDone.")
    if len(unfound) == 0:
        print("All files were found and copied successfully!")
    
    else:
        print("Not all files were found")
        print(f"Missing ({len(unfound)}):\n")
        for title in unfound:
            print(f"\t{title}")
        print(f"\n{'='*70}\n\nFound ({len(found)}):\n")
        for title in found:
            print(f"\t{title}")

    print(conflict)                
 

Main()

#print(getTitle(r"C:\Users\cw1a\Music\BeatSaber\Beat Saber - 029.mp3"))
