import os

class pickotus:
    def __init__(self, infolder, outfolder, rdb="silva"):
        self.infolder = infolder
        self.outfolder = outfolder
        self.rdb = rdb

        assert os.path.isdir(
            self.infolder), "Input folder (%s) does not exist, Please use an existing folder." % self.infolder
        assert not os.path.isdir(
            self.outfolder), "Output folder (%s) does exist, Please do not use an existing folder name." % self.outfolder

    # TODO: not implimented yet.
    def run(self):
        """
        """

        # TODO : add no parallel option

        inFolder = asfolder(inFolder)
        outFolder = asfolder(outFolder)

        inFolder_fasta = inFolder + "*.fasta"
        print("Otu picking...")
        if PR['np']:
            parallel_string = ""
        else:
            parallel_string = "-a -O %d" % PR['number_of_cores']


        if PR['c_ref'] != "none":
            if rdb == "silva":
                execute("pick_open_reference_otus.py -i %s -o %s -p %s -r %s %s -n %s"
                        % (
                            inFolder_fasta, outFolder, PR['parameter_file_name'], PR['c_ref'], parallel_string, PR['c_otu_id']),
                        shell=True)
                #execute("filter_otus_from_otu_table.py -i %s -o %s --negate_ids_to_exclude -e %s"
                #        % (out_folder + "otu_table_mc2_w_tax_no_pynast_failures.biom",
                #           out_folder + "otu_table_mc2_w_tax_no_pynast_failures_close_reference.biom",
                #           PR['silva_reference_seqs']), shell=True)

            elif fungus:
                execute("pick_open_reference_otus.py -i %s -o %s -p %s %s -n %s --suppress_align_and_tree"
                        % (inFolder_fasta, outFolder, PR['parameter_file_name'], parallel_string, PR['c_otu_id']), shell=True)

            else:
                execute("pick_open_reference_otus.py -i %s -o %s -r %s -p %s %s -n %s"
                        % (inFolder_fasta, outFolder,
                           PR['c_ref'], PR['parameter_file_name'],
                           parallel_string, PR['c_otu_id']), shell=True)

                #execute("filter_otus_from_otu_table.py -i %s -o %s --negate_ids_to_exclude -e %s"
                #        % (out_folder + "otu_table_mc2_w_tax_no_pynast_failures.biom",
                #           out_folder + "otu_table_mc2_w_tax_no_pynast_failures_close_reference.biom",
                #           PR['gg_reference_seqs']), shell=True)



        else:
            if rdb == "silva":
                execute("pick_open_reference_otus.py -i %s -o %s -p %s -r %s %s -n %s"
                        % (inFolder_fasta, outFolder, PR['parameter_file_name'], PR['silva_reference_seqs'], parallel_string,
                           PR['c_otu_id']),
                        shell=True)
                execute("filter_otus_from_otu_table.py -i %s -o %s --negate_ids_to_exclude -e %s"
                        % (outFolder + "otu_table_mc2_w_tax_no_pynast_failures.biom",
                           outFolder + "otu_table_mc2_w_tax_no_pynast_failures_close_reference.biom",
                           PR['silva_reference_seqs']), shell=True)

            elif fungus:
                execute("pick_open_reference_otus.py -i %s -o %s -p %s %s -n %s--suppress_align_and_tree"
                        % (inFolder_fasta, outFolder, PR['parameter_file_name'], parallel_string,
                           PR['c_otu_id']), shell=True)

            else:
                execute("pick_open_reference_otus.py -i %s -o %s -r %s -p %s -n %s"
                        % (inFolder_fasta, outFolder,
                           PR['gg_reference_seqs'], PR['parameter_file_name'],
                           parallel_string, PR['c_otu_id']), shell=True)

                execute("filter_otus_from_otu_table.py -i %s -o %s --negate_ids_to_exclude -e %s"
                        % (outFolder + "otu_table_mc2_w_tax_no_pynast_failures.biom",
                           outFolder + "otu_table_mc2_w_tax_no_pynast_failures_close_reference.biom",
                           PR['gg_reference_seqs']), shell=True)

        if PR['remove_intermediate']:
            os.removedirs(inFolder)
