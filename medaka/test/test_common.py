import os
import unittest
import uuid

import medaka.common

class TestMkdir(unittest.TestCase):

    def test_000_directory_created(self):
        dirname = str(uuid.uuid4())
        medaka.common.mkdir_p(dirname)
        self.assertTrue(os.path.exists(dirname))
        os.rmdir(dirname)

    def test_001_directory_not_overwritten(self):
        dirname = str(uuid.uuid4())
        medaka.common.mkdir_p(dirname)
        t0 = os.path.getmtime(dirname)
        medaka.common.mkdir_p(dirname)
        t1 = os.path.getmtime(dirname)
        # time stamp of directory unchanged after calling mkdir_p twice
        self.assertEqual(t0, t1)
        os.rmdir(dirname)

class TestBase2IndexDict(unittest.TestCase):
    def testb2iu(self):
        b2i_dict = medaka.common.base2index
        for idx,character in enumerate('acgtACGTdD'):
            assert b2i_dict[character] == idx


class TestLooseVersionSort(unittest.TestCase):
    def test_sort(self):
        versions = ['1.0.0', '1.0.1', '1.0.10', '1.0.2', '2.0.0', '1.0']
        sorted_versions = medaka.common.loose_version_sort(versions)
        self.assertEqual(sorted_versions, ['1.0', '1.0.0', '1.0.1', '1.0.2', '1.0.10', '2.0.0'])

        versions = ['chr10', 'chr2', 'chr1']
        sorted_versions = medaka.common.loose_version_sort(versions)
        self.assertEqual(sorted_versions, ['chr1', 'chr2', 'chr10'])

        v1 = medaka.vcf.Variant('chr1', 100, 'A', 'C')
        v2 = medaka.vcf.Variant('chr1', 200, 'A', 'C')
        v3 = medaka.vcf.Variant('chr2', 150, 'A', 'C')
        sorted_variants = medaka.common.loose_version_sort([v3, v2, v1],key=lambda v: '{}-{}'.format(v.chrom, v.pos))
        self.assertEqual(sorted_variants, [v1, v2, v3])