#!/usr/bin/env python

import os
import shutil
import mimetypes
import magic
import filecmp
import random
import unittest
from bin.normal_distribution_graph_generator import *
import argparse

OUT_PATH_BASE = "var/tests/data/out/is_normal_distribution"
OUT_PATH_OF_NORMAL_DISTRIBUTION = "{}/{}_loc{}_scale{}_size{}_bins{}.{}"
OUT_PATH_OF_NOT_NORMAL_DISTRIBUTION = "{}/{}_loc{}-{}_scale{}-{}_size{}-{}_bins{}.{}"
NUMBER_FOR_MULTIPLE_FILE_GENERATION = 10


class NormalDistributionGraphGeneratorTest(unittest.TestCase):
    def setUp(self) -> None:
        for name in ['true', 'false']:
            os.makedirs("/".join([OUT_PATH_BASE, name]), exist_ok=True)
        argparser = argparse.ArgumentParser()
        argparser.add_argument('-n', '--number', default=1, help="The number of output files")
        argparser.add_argument('-o', '--out', default="var/data/out/is_normal_distribution", help="Path to output")
        argparser.add_argument('-z', '--zerofill', default=4)
        argparser.add_argument('-f', '--format', default='png', help="The format of output images")
        argparser.add_argument('-l', '--loc', default=50.0)
        argparser.add_argument('-c', '--scale', default=20.0)
        argparser.add_argument('-s', '--size', default=1000)
        argparser.add_argument('-b', '--bins', default=100)
        self.parsed_args = argparser.parse_args(['--number', '1'])
        return super().setUp()
    
    def tearDown(self) -> None:
        for name in ['true', 'false']:
            shutil.rmtree("/".join([OUT_PATH_BASE, name]))
        return super().tearDown()

    def get_params_for_test_generate_normal_distribution_graphs_basic(self):
        out_dir = "/".join([OUT_PATH_BASE, "true"])
        kwargs = {}
        kwargs['number'] = int(self.parsed_args.number)
        kwargs['zerofill'] = int(self.parsed_args.zerofill)
        kwargs['loc'] = float(self.parsed_args.loc)
        kwargs['scale'] = float(self.parsed_args.scale)
        kwargs['size'] = int(self.parsed_args.size)
        kwargs['bins'] = int(self.parsed_args.bins)
        kwargs['suffix'] = self.parsed_args.format
        return out_dir, kwargs

    def call_generate_normal_distribution_graphs(self, out_dir, kwargs) -> None:
        generate_normal_distribution_graphs(out_dir, kwargs['number'], kwargs['zerofill'], kwargs['loc'],
            kwargs['scale'], kwargs['size'], kwargs['bins'], kwargs['suffix'])

    def test_generate_normal_distribution_graphs_basic(self) -> None:
        out_dir, kwargs = self.get_params_for_test_generate_normal_distribution_graphs_basic()

        self.call_generate_normal_distribution_graphs(out_dir, kwargs)

        out = OUT_PATH_OF_NORMAL_DISTRIBUTION.format(out_dir,
            str(kwargs['number']-1).zfill(kwargs['zerofill']),
            kwargs['loc'],
            kwargs['scale'],
            kwargs['size'],
            kwargs['bins'],
            kwargs['suffix'])
        self.assertTrue(os.path.exists(out))

        mimetype = mimetypes.guess_type(out)
        self.assertEqual(mimetype[0], 'image/png')
        mimetype = magic.from_file(out, mime=True)
        self.assertEqual(mimetype, 'image/png')

        num_files = len([name for name in os.listdir(out_dir) if os.path.isfile(os.path.join(out_dir, name))])
        self.assertEqual(num_files, 1)

        not_normal_distribution_graph_generator_test = NotNormalDistributionGraphGeneratorTest()
        not_normal_distribution_graph_generator_test.setUp()
        out_dir_unused, _ = not_normal_distribution_graph_generator_test.get_params_for_test_generate_not_normal_distribution_graphs_basic()
        num_files = len([name for name in os.listdir(out_dir_unused) if os.path.isfile(os.path.join(out_dir_unused, name))])
        self.assertEqual(num_files, 0)
    
    def test_generate_normal_distribution_graphs_on_number_equals_0(self) -> None:
        out_dir, kwargs = self.get_params_for_test_generate_normal_distribution_graphs_basic()
        kwargs['number'] = 0

        self.call_generate_normal_distribution_graphs(out_dir, kwargs)

        num_files = len([name for name in os.listdir(out_dir) if os.path.isfile(os.path.join(out_dir, name))])
        self.assertEqual(num_files, 0)
    
    def test_generate_normal_distribution_graphs_on_number(self) -> None:
        out_dir, kwargs = self.get_params_for_test_generate_normal_distribution_graphs_basic()
        kwargs['number'] = NUMBER_FOR_MULTIPLE_FILE_GENERATION

        self.call_generate_normal_distribution_graphs(out_dir, kwargs)

        for i in range(0, kwargs['number']):
            out = OUT_PATH_OF_NORMAL_DISTRIBUTION.format(out_dir,
                str(i).zfill(kwargs['zerofill']),
                kwargs['loc'],
                kwargs['scale'],
                kwargs['size'],
                kwargs['bins'],
                kwargs['suffix'])
            self.assertTrue(os.path.exists(out))

            mimetype = mimetypes.guess_type(out)
            self.assertEqual(mimetype[0], 'image/png')
            mimetype = magic.from_file(out, mime=True)
            self.assertEqual(mimetype, 'image/png')

            out_next = str()
            if i+1 < kwargs['number']:
                out_next = OUT_PATH_OF_NORMAL_DISTRIBUTION.format(out_dir,
                    str(i+1).zfill(kwargs['zerofill']),
                    kwargs['loc'],
                    kwargs['scale'],
                    kwargs['size'],
                    kwargs['bins'],
                    kwargs['suffix'])
            else:
                out_next = OUT_PATH_OF_NORMAL_DISTRIBUTION.format(out_dir,
                    str(0).zfill(kwargs['zerofill']),
                    kwargs['loc'],
                    kwargs['scale'],
                    kwargs['size'],
                    kwargs['bins'],
                    kwargs['suffix'])
            self.assertFalse(filecmp.cmp(out, out_next, shallow=False))

        num_files = len([name for name in os.listdir(out_dir) if os.path.isfile(os.path.join(out_dir, name))])
        self.assertEqual(num_files, NUMBER_FOR_MULTIPLE_FILE_GENERATION)

    def test_generate_normal_distribution_graphs_on_zerofill(self) -> None:
        out_dir, kwargs = self.get_params_for_test_generate_normal_distribution_graphs_basic()
        kwargs['zerofill'] = random.choice(range(2, 100))

        self.call_generate_normal_distribution_graphs(out_dir, kwargs)

        out = OUT_PATH_OF_NORMAL_DISTRIBUTION.format(out_dir,
            str(kwargs['number']-1).zfill(kwargs['zerofill']),
            kwargs['loc'],
            kwargs['scale'],
            kwargs['size'],
            kwargs['bins'],
            kwargs['suffix'])
        self.assertTrue(os.path.exists(out))

    def test_generate_normal_distribution_graphs_on_zerofill_equals_0(self) -> None:
        out_dir, kwargs = self.get_params_for_test_generate_normal_distribution_graphs_basic()
        kwargs['zerofill'] = 0

        self.call_generate_normal_distribution_graphs(out_dir, kwargs)

        out = OUT_PATH_OF_NORMAL_DISTRIBUTION.format(out_dir,
            str(kwargs['number']-1),
            kwargs['loc'],
            kwargs['scale'],
            kwargs['size'],
            kwargs['bins'],
            kwargs['suffix'])
        self.assertTrue(os.path.exists(out))

    def test_generate_normal_distribution_graphs_format_equals_jpg(self) -> None:
        out_dir, kwargs = self.get_params_for_test_generate_normal_distribution_graphs_basic()
        kwargs['suffix'] = 'jpg'

        self.call_generate_normal_distribution_graphs(out_dir, kwargs)

        out = OUT_PATH_OF_NORMAL_DISTRIBUTION.format(out_dir,
            str(kwargs['number']-1).zfill(kwargs['zerofill']),
            kwargs['loc'],
            kwargs['scale'],
            kwargs['size'],
            kwargs['bins'],
            kwargs['suffix'])
        self.assertTrue(os.path.exists(out))

        mimetype = mimetypes.guess_type(out)
        self.assertEqual(mimetype[0], 'image/jpeg')
        mimetype = magic.from_file(out, mime=True)
        self.assertEqual(mimetype, 'image/jpeg')

    def test_generate_normal_distribution_graphs_format_equals_tiff(self) -> None:
        out_dir, kwargs = self.get_params_for_test_generate_normal_distribution_graphs_basic()
        kwargs['suffix'] = 'tiff'

        self.call_generate_normal_distribution_graphs(out_dir, kwargs)

        out = OUT_PATH_OF_NORMAL_DISTRIBUTION.format(out_dir,
            str(kwargs['number']-1).zfill(kwargs['zerofill']),
            kwargs['loc'],
            kwargs['scale'],
            kwargs['size'],
            kwargs['bins'],
            kwargs['suffix'])
        self.assertTrue(os.path.exists(out))

        mimetype = mimetypes.guess_type(out)
        self.assertEqual(mimetype[0], 'image/tiff')
        mimetype = magic.from_file(out, mime=True)
        self.assertEqual(mimetype, 'image/tiff')


class NotNormalDistributionGraphGeneratorTest(unittest.TestCase):
    def setUp(self) -> None:
        for name in ['true', 'false']:
            os.makedirs("/".join([OUT_PATH_BASE, name]), exist_ok=True)
        argparser = argparse.ArgumentParser()
        argparser.add_argument('-n', '--number', default=1, help="The number of output files")
        argparser.add_argument('-o', '--out', default="var/data/out/is_normal_distribution", help="Path to output")
        argparser.add_argument('-z', '--zerofill', default=4)
        argparser.add_argument('-f', '--format', default='png', help="The format of output images")
        argparser.add_argument('-b', '--bins', default=100)
        argparser.add_argument('--loc1', default=25.0)
        argparser.add_argument('--loc2', default=75.0)
        argparser.add_argument('--scale1', default=20.0)
        argparser.add_argument('--scale2', default=20.0)
        argparser.add_argument('--size1', default=500)
        argparser.add_argument('--size2', default=500)
        self.parsed_args = argparser.parse_args(['--number', '1'])
        return super().setUp()
    
    def tearDown(self) -> None:
        for name in ['true', 'false']:
            shutil.rmtree("/".join([OUT_PATH_BASE, name]))
        return super().tearDown()
    
    def get_params_for_test_generate_not_normal_distribution_graphs_basic(self):
        out_dir = "/".join([OUT_PATH_BASE, "false"])
        kwargs = {}
        kwargs['number'] = int(self.parsed_args.number)
        kwargs['zerofill'] = int(self.parsed_args.zerofill)
        kwargs['loc1'] = float(self.parsed_args.loc1)
        kwargs['scale1'] = float(self.parsed_args.scale1)
        kwargs['size1'] = int(self.parsed_args.size1)
        kwargs['loc2'] = float(self.parsed_args.loc2)
        kwargs['scale2'] = float(self.parsed_args.scale2)
        kwargs['size2'] = int(self.parsed_args.size2)
        kwargs['bins'] = int(self.parsed_args.bins)
        kwargs['suffix'] = self.parsed_args.format
        return out_dir, kwargs

    def call_generate_not_normal_distribution_graphs(self, out_dir, kwargs) -> None:
        generate_not_normal_distribution_graphs(out_dir, kwargs['number'], kwargs['zerofill'],
            kwargs['loc1'], kwargs['loc2'], kwargs['scale1'], kwargs['scale2'], kwargs['size1'], kwargs['size2'],
            kwargs['bins'], kwargs['suffix'])

    def test_generate_not_normal_distribution_graphs_basic(self) -> None:
        out_dir, kwargs = self.get_params_for_test_generate_not_normal_distribution_graphs_basic()

        self.call_generate_not_normal_distribution_graphs(out_dir, kwargs)

        out = OUT_PATH_OF_NOT_NORMAL_DISTRIBUTION.format(out_dir,
            str(kwargs['number']-1).zfill(kwargs['zerofill']),
            kwargs['loc1'],
            kwargs['loc2'],
            kwargs['scale1'],
            kwargs['scale2'],
            kwargs['size1'],
            kwargs['size2'],
            kwargs['bins'],
            kwargs['suffix'])
        self.assertTrue(os.path.exists(out))

        mimetype = mimetypes.guess_type(out)
        self.assertEqual(mimetype[0], 'image/png')
        mimetype = magic.from_file(out, mime=True)
        self.assertEqual(mimetype, 'image/png')

        num_files = len([name for name in os.listdir(out_dir) if os.path.isfile(os.path.join(out_dir, name))])
        self.assertEqual(num_files, 1)

        normal_distribution_graph_generator_test = NormalDistributionGraphGeneratorTest()
        normal_distribution_graph_generator_test.setUp()
        out_dir_unused, _ = normal_distribution_graph_generator_test.get_params_for_test_generate_normal_distribution_graphs_basic()
        num_files = len([name for name in os.listdir(out_dir_unused) if os.path.isfile(os.path.join(out_dir_unused, name))])
        self.assertEqual(num_files, 0)

    def test_generate_not_normal_distribution_graphs_on_number_equals_0(self) -> None:
        out_dir, kwargs = self.get_params_for_test_generate_not_normal_distribution_graphs_basic()
        kwargs['number'] = 0

        self.call_generate_not_normal_distribution_graphs(out_dir, kwargs)

        num_files = len([name for name in os.listdir(out_dir) if os.path.isfile(os.path.join(out_dir, name))])
        self.assertEqual(num_files, 0)

    def test_generate_not_normal_distribution_graphs_on_number(self) -> None:
        out_dir, kwargs = self.get_params_for_test_generate_not_normal_distribution_graphs_basic()
        kwargs['number'] = NUMBER_FOR_MULTIPLE_FILE_GENERATION

        self.call_generate_not_normal_distribution_graphs(out_dir, kwargs)

        for i in range(0, kwargs['number']):
            out = OUT_PATH_OF_NOT_NORMAL_DISTRIBUTION.format(out_dir,
                str(i).zfill(kwargs['zerofill']),
                kwargs['loc1'],
                kwargs['loc2'],
                kwargs['scale1'],
                kwargs['scale2'],
                kwargs['size1'],
                kwargs['size2'],
                kwargs['bins'],
                kwargs['suffix'])
            self.assertTrue(os.path.exists(out))

            mimetype = mimetypes.guess_type(out)
            self.assertEqual(mimetype[0], 'image/png')
            mimetype = magic.from_file(out, mime=True)
            self.assertEqual(mimetype, 'image/png')

            out_next = str()
            if i+1 < kwargs['number']:
                out_next = OUT_PATH_OF_NOT_NORMAL_DISTRIBUTION.format(out_dir,
                    str(i+1).zfill(kwargs['zerofill']),
                    kwargs['loc1'],
                    kwargs['loc2'],
                    kwargs['scale1'],
                    kwargs['scale2'],
                    kwargs['size1'],
                    kwargs['size2'],
                    kwargs['bins'],
                    kwargs['suffix'])
            else:
                out_next = OUT_PATH_OF_NOT_NORMAL_DISTRIBUTION.format(out_dir,
                    str(0).zfill(kwargs['zerofill']),
                    kwargs['loc1'],
                    kwargs['loc2'],
                    kwargs['scale1'],
                    kwargs['scale2'],
                    kwargs['size1'],
                    kwargs['size2'],
                    kwargs['bins'],
                    kwargs['suffix'])
            self.assertFalse(filecmp.cmp(out, out_next, shallow=False))

        num_files = len([name for name in os.listdir(out_dir) if os.path.isfile(os.path.join(out_dir, name))])
        self.assertEqual(num_files, NUMBER_FOR_MULTIPLE_FILE_GENERATION)

    def test_generate_not_normal_distribution_graphs_on_zerofill(self) -> None:
        out_dir, kwargs = self.get_params_for_test_generate_not_normal_distribution_graphs_basic()
        kwargs['zerofill'] = random.choice(range(2, 100))

        self.call_generate_not_normal_distribution_graphs(out_dir, kwargs)

        out = OUT_PATH_OF_NOT_NORMAL_DISTRIBUTION.format(out_dir,
            str(kwargs['number']-1).zfill(kwargs['zerofill']),
            kwargs['loc1'],
            kwargs['loc2'],
            kwargs['scale1'],
            kwargs['scale2'],
            kwargs['size1'],
            kwargs['size2'],
            kwargs['bins'],
            kwargs['suffix'])
        self.assertTrue(os.path.exists(out))

    def test_generate_not_normal_distribution_graphs_on_zerofill_equals_0(self) -> None:
        out_dir, kwargs = self.get_params_for_test_generate_not_normal_distribution_graphs_basic()
        kwargs['zerofill'] = 0

        self.call_generate_not_normal_distribution_graphs(out_dir, kwargs)

        out = OUT_PATH_OF_NOT_NORMAL_DISTRIBUTION.format(out_dir,
            str(kwargs['number']-1),
            kwargs['loc1'],
            kwargs['loc2'],
            kwargs['scale1'],
            kwargs['scale2'],
            kwargs['size1'],
            kwargs['size2'],
            kwargs['bins'],
            kwargs['suffix'])
        self.assertTrue(os.path.exists(out))

    def test_generate_not_normal_distribution_graphs_format_equals_jpg(self) -> None:
        out_dir, kwargs = self.get_params_for_test_generate_not_normal_distribution_graphs_basic()
        kwargs['suffix'] = 'jpg'

        self.call_generate_not_normal_distribution_graphs(out_dir, kwargs)

        out = OUT_PATH_OF_NOT_NORMAL_DISTRIBUTION.format(out_dir,
            str(kwargs['number']-1).zfill(kwargs['zerofill']),
            kwargs['loc1'],
            kwargs['loc2'],
            kwargs['scale1'],
            kwargs['scale2'],
            kwargs['size1'],
            kwargs['size2'],
            kwargs['bins'],
            kwargs['suffix'])
        self.assertTrue(os.path.exists(out))

        mimetype = mimetypes.guess_type(out)
        self.assertEqual(mimetype[0], 'image/jpeg')
        mimetype = magic.from_file(out, mime=True)
        self.assertEqual(mimetype, 'image/jpeg')

    def test_generate_not_normal_distribution_graphs_format_equals_tiff(self) -> None:
        out_dir, kwargs = self.get_params_for_test_generate_not_normal_distribution_graphs_basic()
        kwargs['suffix'] = 'tiff'

        self.call_generate_not_normal_distribution_graphs(out_dir, kwargs)

        out = OUT_PATH_OF_NOT_NORMAL_DISTRIBUTION.format(out_dir,
            str(kwargs['number']-1).zfill(kwargs['zerofill']),
            kwargs['loc1'],
            kwargs['loc2'],
            kwargs['scale1'],
            kwargs['scale2'],
            kwargs['size1'],
            kwargs['size2'],
            kwargs['bins'],
            kwargs['suffix'])
        self.assertTrue(os.path.exists(out))

        mimetype = mimetypes.guess_type(out)
        self.assertEqual(mimetype[0], 'image/tiff')
        mimetype = magic.from_file(out, mime=True)
        self.assertEqual(mimetype, 'image/tiff')


if __name__ == '__main__':
    unittest.main()
