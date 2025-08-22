import os

filename = r"CurrentSys2.png"
filepath = r"D:\Computer Science\CurrentSys2.png"
dir = r"D:\Computer Science\ISLAM_WEB"

new_path = os.path.join(dir, filename)
os.rename(filepath, new_path)

print(new_path)