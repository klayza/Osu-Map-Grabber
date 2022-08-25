import os
import shutil

# Deletes folder with music in them and skips the ones without in the event extractor.py doesn't work
# Relevant if debugging extractor
# 

music_folder = "C:/Users/cw1a/Music/Osu!"
accepted_song_types = [".mp3", ".ogg"]

def containsMusic(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for f_type in accepted_song_types:
            if f_type in str(files):
                return True
    return False

def main():
    deleted = 0
    skipped = 0
    folders = os.listdir(music_folder)
    print(f"Starting work on {len(folders)} folders\n{'-'*40}")
    for folder in folders:
        index = str(folders.index(folder) + 1)
        source = f"{music_folder}/{folder}"
        if containsMusic(source):
            print(f"{index} | Deleting folder: {source}")
            shutil.rmtree(source)
            deleted += 1
        else: 
            print(f"{index} | Skipping folder: {source}")
            skipped += 1
    
    print(f"\nFinished.\nDeleted {deleted} of {len(folders)} folders\nSkipped {skipped} of {len(folders)} folders")

main()