import gzip
import os

from Bio import SeqIO


class TrimFolder:
    def __init__(self, infolder:PairedFolder, outfolder:str, method):
        self.infolder =infolder
        self.outfolder = outfolder
        self.method = method

    def primertrim(self, input_fastq_file, output_fastq_file, length):
        """
        Trim primer sequence

        Parameters
        ----------
        input_fastq_file: str
            input file (fastq)
        output_fastq_file: str
            output file (fastq)
        length:
            trimming length

        Returns
        -------
            None

        Examples
        --------
        >>> primertrim("/fastq/sample1_R1_L001.fastq",
                "/trimmedfastq/sample1_R1_L001.fastq", 12)

        >>> primertrim("/fastq/sample1_R2_L001.fastq",
                "/trimmedfastq/sample1_R2_L001.fastq", 12)
        """
        assert os.path.isfile(input_fastq_file), "%s does not exist" % input_fastq_file
        assert not os.path.isfile(output_fastq_file), "%s is exist" % output_fastq_file

        if input_fastq_file.endswith(".gz"):
            infq = gzip.open(input_fastq_file, "rt")
        else:
            infq = open(input_fastq_file, "rt")
        if output_fastq_file.endswith(".gz"):
            outfq = gzip.open(output_fastq_file, "wb")
        else:
            outfq = open(output_fastq_file, "wb")

        trimmed = [record[length:] for record in SeqIO.parse(infq, "fastq")]
        SeqIO.write(trimmed, outfq, "fastq")

        infq.close()
        outfq.close()


    def trim(input_folder, output_folder, trim_quality_threshold, trim_prime=True):
        """
        Quality trimming of Fastq files.

        Parameters
        ----------
        input_folder :  str
            Full path for the input folder
        output_folder: str
            Full path for the output folder
        trim_quality_threshold: int
            Regions with average quality BELOW this will be trimmed.
        trim_prime: bool
            if True: prime sequence is trimmed.

        Returns
        -------
            None

        Side
        """

        inFolder = asfolder(inFolder)
        outFolder = asfolder(outFolder)

        assert os.path.isdir(inFolder), "%s does not exist" % inFolder
        assert not os.path.isdir(outFolder), "%s exists, use a new folder [recommended]" % outFolder

        files = os.listdir(inFolder)
        files.sort()

        ins1 = [x for x in files if "_R1_" in x]
        ins2 = [x.replace("_R1_", "_R2_") for x in ins1]
        os.mkdir(outFolder)
        print("Trimming...")
        def trim_process(i):
            in1 = inFolder + ins1[i]
            in2 = inFolder + ins2[i]
            print("\n%s and %s" % (ins1[i], ins2[i]))
            out1 = outFolder + ins1[i]
            out2 = outFolder + ins2[i]
            out1_temp1 = outFolder + "temp1_" + ins1[i]
            out2_temp1 = outFolder + "temp1_" + ins2[i]

            if trim_prime:
                primertrim(in1, out1_temp1, 17)
                primertrim(in2, out2_temp1, 21)

            else:
                out1_temp1 = in1
                out2_temp1 = in2

            if PR['adapter_ref'] != None:

                execute(
                    "bbduk.sh -Xmx1000m -in1=%s -in2=%s -out1=%s -out2=%s -outm=stdout.fa -ref=%s -qtrim=r -trimq=%d -k=18 -ktrim=f" %
                    (out1_temp1, out2_temp1, out1, out2, PR['adapter_ref'], trimq), shell=True)
            else:
                execute(
                    "bbduk.sh -Xmx1000m -in1=%s -in2=%s -out1=%s -out2=%s -qtrim=r -trimq=%d" %
                    (out1_temp1, out2_temp1, out1, out2, trimq), shell=True)

            os.remove(out1_temp1)
            os.remove(out2_temp1)

        p = Pool(PR['number_of_cores'])
        p.map(trim_process, range(len(ins1)))