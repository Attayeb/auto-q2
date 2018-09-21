from subprocess import Popen, PIPE
import logging
import configparser
import os

def loginfo(message):
    """
    save information to log file
    :param message: saved to log file
    :type message: str
    :return:
    """
    logging.info(message.encode('utf-8'))


def logwarning(message):
    logging.warning(message.encode('utf-8'))


def execute(command, shell=True):
    """
    Execute command using os package and return output to log file
    :param command: The command to be executed
    :type command: str
    :param shell: Takes either True or False
    :type shell: boolean
    :return: Run the command in the background and save the
    output to the logging file.
    """
    loginfo(command)
    p = Popen(command.split(), stderr=PIPE, stdout=PIPE)
    output, error = p.communicate()
    if output != b"":
        loginfo(output.encode('utf-8'))
    if error != b"":
        logwarning(error.encode('utf-8'))


def write_parameter_file(parameter_file, PR):
    """
    :param parameter_file:
    :return:
    """

    if PR['rdb'] == "silva":
        parameter_string = """
    assign_taxonomy:id_to_taxonomy_fp\t%(taxonomy)s
    assign_taxonomy:reference_seqs_fp\t%(reference_seqs)s
    pick_otus.py:pick_otus_reference_seqs_fp\t%(reference_seqs)s
    pick_otus:enable_rev_strand_match True
    filter_alignment.py:pynast_template_alignment_fp\t%(core_alignment)s
    parallel:jobs_to_start\t%(jobs_to_start)d
    assign_taxonomy:similarity\t%(similarity)s
    """ % {'taxonomy': PR['silva_taxonomy'],
           'reference_seqs': PR['silva_reference_seqs'],
           'core_alignment': PR['silva_core_alignment'],
           'jobs_to_start': PR['number_of_cores'],
           'similarity': PR['similarity']}
    elif PR['rdb'] == "unite":
        # pass
        parameter_string = """
        assign_taxonomy:id_to_taxonomy_fp\t%(taxonomy)s
        assign_taxonomy:reference_seqs_fp\t%(reference_seqs)s
        pick_otus.py:pick_otus_reference_seqs_fp\t%(reference_seqs)s
        parallel:jobs_to_start\t%(jobs_to_start)d
        assign_taxonomy:assignment_method blast
        # should we use e_value or blast_e_value
        parallel_assign_taxonomy_blast:e_value\t%(blast_e_value)s
        # comment
        """ % {'taxonomy': PR['unite_taxonomy'],
               'reference_seqs': PR['unite_reference_seqs'],
               'jobs_to_start': PR['number_of_cores'],
               'blast_e_value': PR['blast_e_value']}
    else:
        parameter_string = '''
    assign_taxonomy:id_to_taxonomy_fp\t%(taxonomy)s
    assign_taxonomy:reference_seqs_fp\t%(reference_seqs)s
    pick_otus.py:pick_otus_reference_seqs_fp\t%(reference_seqs)s
    pick_otus:enable_rev_strand_match True
    filter_alignment.py:pynast_template_alignment_fp\t%(core_alignment)s
    parallel:jobs_to_start\t%(jobs_to_start)d
    assign_taxonomy:similarity\t%(similarity)s
    ''' % {'taxonomy': PR['gg_taxonomy'],
           'reference_seqs': PR['gg_reference_seqs'],
           'core_alignment': PR['gg_core_alignment'],
           'jobs_to_start': PR['number_of_cores'],
           'similarity': PR['similarity']}
    os.mkdir(PR['others'])

    f = open(parameter_file, "w")
    f.write(parameter_string)
    f.close()


def get_configuration(PR):
    cp = configparser.ConfigParser()
    cp.read(PR['ConfigFile'])
    PR['Ftrimmed'] = asfolder(cp.get('FOLDERS', 'trimmed'))
    PR['Fmerged'] = asfolder(cp.get('FOLDERS', 'merged'))
    PR['Fqc'] = asfolder(cp.get('FOLDERS', 'quality_step'))
    PR['Fchi'] = asfolder(cp.get('FOLDERS', 'chimera_removed'))
    PR['Fotus'] = asfolder(cp.get('FOLDERS', 'otus'))
    PR['Fdiv'] = asfolder(cp.get('FOLDERS', 'diversity_analyses'))
    PR['Fothers'] = asfolder(cp.get('FOLDERS', 'others'))
    PR['number_of_cores'] = int(cp.get('GENERAL', 'jobs_to_start'))
    PR['silva_taxonomy'] = cp.get('SILVA', 'taxonomy')
    PR['silva_reference_seqs'] = cp.get('SILVA', 'reference_seqs')
    PR['silva_core_alignment'] = cp.get('SILVA', 'core_alignment')
    PR['silva_chim_ref'] = cp.get('CHIMERA', 'silva')
    PR['gg_taxonomy'] = cp.get('GG', 'taxonomy')
    PR['gg_reference_seqs'] = cp.get('GG', 'reference_seqs')
    PR['gg_core_alignment'] = cp.get('GG', 'core_alignment')
    PR['gg_chim_ref'] = cp.get('CHIMERA', 'gg')
    PR['unite_taxonomy'] = cp.get('UNITE', 'taxonomy')
    PR['unite_reference_seqs'] = cp.get('UNITE', 'reference_seqs')
    PR['similarity'] = cp.get('GENERAL', 'similarity')
    PR['blast_e_value'] = cp.get('GENERAL', 'blast_e_value')
    PR['bbmap_resources'] = cp.get('bbmap', 'resources')


def remove_short_reads(infqfile, outfqfile, length):
    """
    :param infqfile: input fastq file name.
    :type infqfile: str
    :param outfqfile: output fastq file name, after removing short reads.
    :type outfqfile: str
    :param length: minimum reads length.
    :type length: int
    :rtype: None
    :return: None
    @Action: filter fastq files removing short reads
    """

    # //TODO rewrite this function using biopython
    infq = open(infqfile, "r")
    outfq = open(outfqfile, "w")
    lines = infq.readlines()
    for a, b, c, d in zip(lines[0::4], lines[1::4], lines[2::4], lines[3::4]):
        if len(b) > length:
            outfq.write(a)
            outfq.write(b)
            outfq.write(c)
            outfq.write(d)

    infq.close()
    outfq.close()

    def asfolder(folder):
        """
        Add "/" at the end of the folder if not inserted
        :param folder: the folder name
        :type folder: str
        :return: file names with / at the end
        :rtype: str
        """
        if folder[-1] != "/":
            return (folder + "/")
        else:
            return (folder)