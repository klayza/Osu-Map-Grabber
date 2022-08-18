import os

source = "C:/Users/cw1a/Music/Osu!"
print("Folders with missing images:")
for folder in os.listdir(source):
    for root, dirs, files in os.walk(f"{source}/{folder}"):
        if ".jpeg" and ".png" and ".jpg" not in str(files):
            print(root)
            break
