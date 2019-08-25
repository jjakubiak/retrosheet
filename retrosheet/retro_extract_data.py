
import os
import zipfile

for filename in os.listdir("c:/retrosheet/downloads/zipped"):
    if filename.endswith(".zip"):
        file_path = "c:/retrosheet/downloads/zipped/{}".format(filename)
        print(file_path)
        with zipfile.ZipFile(file_path,"r") as zip_ref:
            zip_ref.extractall("c:/retrosheet/downloads/unzipped")


