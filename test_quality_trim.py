import unittest
from os.path import join as osaspath
import os
from quality_trim import primertrim, trim

class QualityTrimTest(unittest.TestCase):
    def test_quality_trim(self):
        primertrim("test/S1_R1_3.fastq", "test/S1_R1_3_result.fastq", 12)
        os.remove(osaspath("test","S1_R1_3_result.fastq"))


if __name__ == "__main__":
    unittest.main()