import os

from common import execute
from multiprocessing.dummy import Pool

#TODO not finished yet.
class quality_control():
    def __init__(self,
                 infolder,
                 outfolder,
                 quality,
                 remove_intermediate=False,
                 number_of_cores=1):
        self.infolder = infolder
        self.outfolder = outfolder
        self.quality = quality
        self.remove_intermediate = remove_intermediate
        self.number_of_cores = number_of_cores

        assert os.path.isdir(
            self.infolder), "Input folder (%s) does not exist, Please use an existing folder." % self.infolder
        assert not os.path.isdir(
            self.outfolder), "Output folder (%s) does exist, Please do not use an existing folder name." % self.outfolder
        self.files = os.listdir(self.infolder)
        self.files.sort()


    def run(self):

        os.mkdir(self.outfolder)

        def quality_control_process(i):
            temp = os.path.join(self.outfolder, "temp"+i)
            print("\nQuality control: %s" % i)
            sampleId = i.replace(".fastq", "")
            infile = os.path.join(self.infolder,  i)
            outfile = os.path.join(self.outfolder, i.replace(".fastq", ".fasta"))
            execute("""split_libraries_fastq.py -i %s -o %s --barcode_type not-barcoded --sample_ids %s -q %s""" % (
                infile, temp, sampleId, self.quality), shell=True)

            tempfile = temp + "seqs.fna"
            os.rename(tempfile, outfile)
            os.remove(temp)
            if self.remove_intermediate:
                os.remove(infile)


        p = Pool(self.number_of_cores)
        p.map(quality_control_process, self.files)
        print("Quality control finished.")
        if self.remove_intermediate:
            os.removedirs(inFolder)

class removechimera():
    def __init__(self,
                 infolder,
                 outfolder,
                 rdb="silva",
                 number_of_cores=1,
                 remove_intermediate=False):
        self.infolder = infolder
        self.outfolder = outfolder
        self.rdb = rdb
        self.number_of_cores = number_of_cores
        self.remove_intermediate = remove_intermediate

        assert os.path.isdir(
            self.infolder), "Input folder (%s) does not exist, Please use an existing folder." % self.infolder
        assert not os.path.isdir(
            self.outfolder), "Output folder (%s) does exist, Please do not use an existing folder name." % self.outfolder
        self.files = os.listdir(infolder)
        self.sort()
        os.mkdir(self.outfoldr)



    def run(self):

        def remove_chimera_process(i):
            print("Chimera removal: %s" % i)
            temp = os.path.join(self.outfolder,  "temp" + i)
            if self.rdb == "silva":
                execute("identify_chimeric_seqs.py -i %s -m usearch61 -o %s -r %s"
                        % (self.infolder + i, temp + i, PR['silva_chim_ref']),
                        shell=True)
            else:
                execute("identify_chimeric_seqs.py -i %s -m usearch61 -o %s -r %s" % (
                    os.path.join(self.infolder, i), temp + i, PR['gg_chim_ref']),
                        shell=True)

            execute("filter_fasta.py -f %s -o %s -s %s/non_chimeras.txt" % (os.path.join(self.infolder, i), os.path.join(self.outfolder, i), temp + i),
                    shell=True)
            call("rm -r %s" % temp, shell=True)
            if PR['remove_intermediate']:
                os.remove(os.path.join(self.infolder, i))

        p = Pool(self.number_of_cores)
        p.map(remove_chimera_process, self.files)
        if PR['remove_intermediate']:
            os.removedirs(infolder)