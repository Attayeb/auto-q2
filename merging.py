import os
from common import execute, loginfo, logwarning, remove_short_reads
from multiprocessing.dummy import Pool
from re import sub


class MergeFolder():
    def __init__(self, infolder, outfolder,
                 method="fastq-join",
                 percentage_of_mismatch=16,
                 maxloose=False,
                 remove_intermediate=False,
                 number_of_cores=1,
                 minimum_length=250):
        self.infolder = infolder
        self.outfolder = outfolder
        self.method = method
        assert os.path.isdir(
            self.infolder), "Input folder (%s) does not exist, Please use an existing folder." % self.infolder
        assert not os.path.isdir(
            self.outfolder), "Output folder (%s) does exist, Please do not use an existing folder name." % self.outfolder
        self.files = os.listdir(infolder)
        self.ins1 = [x for x in self.files if "_R1_" in x]
        self.ins2 = [x.replace("_R1_", "_R2_") for x in self.ins1]
        self.outs = [x.replace("_L001_R1_001", "") for x in self.ins1]
        self.maxloose = maxloose
        self.remove_intermediate = remove_intermediate
        self.number_of_cores = number_of_cores
        self.percentage_of_mismacth = percentage_of_mismatch
        self.minimum_length= minimum_length

    def merge(self):
        if self.method == "fastq-join":
            self.__mergefolderfastq()
        elif self.method == "bbmerge":
            self.__mergefolderbb()

    def __mergefolderbb(self):
        """
        """

        os.mkdir(self.outfolder)
        print("\nMerging ...")

        def mergefolderbb_process(i):

            in1 = os.path.join(self.infolder, self.ins1[i])
            in2 = os.path.join(self.infolder, self.ins2[i])

            print("%s and %s" % (self.ins1[i], self.ins2[i]))
            out = os.path.join(self.outfolder + self.outs[i])
            if self.maxloose:
                execute(
                    "bbmerge.sh -in1={in1} -in2={in2} -out={out} -maxloose=t -ignorebadquality".format(in1=in1, in2=in2,
                                                                                                       out=out),
                    shell=True)

            else:
                execute("bbmerge.sh -in1= -in2=%s -out=%s -ignorebadquality" % (in1, in2, out), shell=True)

            if self.remove_intermediate:
                os.remove(self.in1)
                os.remove(self.in2)

        p = Pool(self.number_of_cores)
        p.map(mergefolderbb_process, range(len(self.ins1)))
        if self.remove_intermediate:
            os.removedirs(self.infolder)
        print("Merging finished.")

    def __mergefolderfastq(self):
        """
        """

        os.mkdir(self.outfolder)

        def process(i):
            in1 = os.path.join(self.infolder + self.ins1[i])
            in2 = os.path.join(self.outfolder + self.ins2[i])
            print("Merging: %s and %s " % (self.ins1[i], self.ins2[i]))
            out = os.path.join(self.outfolder, "temp_" + self.outs[i])
            out_final = os.path.join(self.outfolder, self.outs[i])
            if out_final.endswith(".gz"):
                out_final = sub(".gz", "", out_final)
            execute("fastq-join -p {percentage_of_mismatch} {in1} {in2} -o {out}".
                    formta(percentage_of_mismatch=self.percentage_of_mismatch, in1=in1, in2=in2, out=out), shell=True)
            os.remove("%sun1" % out)
            os.remove("%sun2" % out)
            os.rename("%sjoin" % out, out)
            remove_short_reads(out, out_final, self.minimum_length)
            os.remove(out)
            if self.remove_intermediate:
                os.remove(in1)
                os.remove(in2)

        p = Pool(self.number_of_cores)
        p.map(process, range(len(self.ins1)))
        if self.remove_intermediate:
            os.removedirs(self.infolder)
