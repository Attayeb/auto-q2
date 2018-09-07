import click

from classes import SingleFolder, PairedFolder

@click.command()
@click.option("--i-input-folder", 'input_folder', prompt="What is the input folder? ")
@click.option("--o-output-folder", 'output_folder', prompt="What is the output folder? ")
@click.option("--t-trimming-threshold", 't_trimming_threshold')
@click.option("--m-merging_method", 'm_merging_method')
@click.option("--fastq-p", 'fastq_p')
@click.option("--q-quality-threshold", 'quality_threshold')
def main(input_folder):
    print(input_folder)


if __name__ == "__main__":
    main()
