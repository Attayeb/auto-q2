from os.path import join
import os
from os import listdir


class PairedFolder:
    def __init__(self, path, type):
        self.path = os.path.abspath(path)
        self.type = type
        files = listdir(self.path)
        files.sort()
        self.files = files
        self.R1 = [x for x in files if "R1" in x]
        self.R2 = [x.replace("R1", "R2") for x in self.R1]
        assert all((x.replace("R1", "R2") in self.R2 for x in self.files)), "%s is not appropriate folder" % self.path
        assert self.type in ['raw', 'trimmed'], "%s is not correct type" % self.type
        self.len = len(files)
        self.R1_len = len(self.R1)
        self.R2_len = len(self.R2)


class SingleFolder:
    def __init__(self, path, type):
        self.path = os.path.abspath(path)
        self.type = type

        files = listdir(self.path)
        files.sort()
        self.files = files
        self.len = len(files)
        assert self.type in ['merged', 'qc', 'chimera_removed'], "%s is not correct type" % self.type



if __name__ == "__main__":
    folderstring = "/media/attayeb/storage/KCAP2/Samples"
    print(os.path.abspath(folderstring))

    folder = '/media/attayeb/storage/KCAP2/Samples'
    in_folder = PairedFolder(folder, "raw")
    in_folder2 = SingleFolder(folder, "merged")
    files = in_folder.files
    print(in_folder2.files)
    print(in_folder2.len)

