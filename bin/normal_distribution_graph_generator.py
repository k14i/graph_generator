#!/usr/bin/env python

import argparse
import numpy as np
import matplotlib.pyplot as plt


def generate_normal_distribution_graphs(out_path_base, number, zerofill, loc, scale, size, bins, suffix):
    for i in range(0, int(number)):
        fig = plt.figure()

        data = np.random.normal(loc=loc, scale=scale, size=size)
        plt.hist(data, bins=bins, color='black')

        fig.patch.set_facecolor('white')

        filename = "{}/{}_loc{}_scale{}_size{}_bins{}.{}".format(
            out_path_base, str(i).zfill(zerofill), loc, scale, size, bins, suffix)
        print("{}/{} {}".format(i+1, number, filename))
        fig.savefig(filename)

def generate_not_normal_distribution_graphs(out_path_base, number, zerofill, loc1, loc2, scale1, scale2, size1, size2, bins, suffix):
    for i in range(0, int(number)):
        fig = plt.figure()

        data = np.concatenate(
            [
                np.random.normal(loc=loc1, scale=scale1, size=size1),
                np.random.normal(loc=loc2, scale=scale2, size=size2)
            ]
        )
        plt.hist(data, bins=bins, color='black')

        fig.patch.set_facecolor('white')

        filename = "{}/{}_loc{}-{}_scale{}-{}_size{}-{}_bins{}.{}".format(
            out_path_base, str(i).zfill(zerofill), loc1, loc2, scale1, scale2, size1, size2, bins, suffix)
        print("{}/{} {}".format(i+1, number, filename))
        fig.savefig(filename)

def generate_graphs(**kwargs):
    label = str(kwargs['is_normal_distribution']).lower()
    out_path_base = "{}/{}".format(kwargs['out'], label)
    if kwargs['is_normal_distribution']:
        generate_normal_distribution_graphs(out_path_base, kwargs['number'], kwargs['zerofill'],
            kwargs['loc'], kwargs['scale'], kwargs['size'],
            kwargs['bins'], kwargs['suffix'])
    else:
        generate_not_normal_distribution_graphs(out_path_base, kwargs['number'], kwargs['zerofill'],
            kwargs['loc1'], kwargs['loc2'], kwargs['scale1'], kwargs['scale2'], kwargs['size1'], kwargs['size2'],
            kwargs['bins'], kwargs['suffix'])

def get_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-t', '--type', default='both', help="Type of graph curves (1, 2, both)")
    argparser.add_argument('-n', '--number', default=1, help="The number of output files")
    argparser.add_argument('-o', '--out', default="var/data/out/is_normal_distribution", help="Path to output")
    argparser.add_argument('-z', '--zerofill', default=4)
    argparser.add_argument('-f', '--format', default='png', help="The format of output images")
    argparser.add_argument('-l', '--loc', default=50.0)
    argparser.add_argument('-c', '--scale', default=20.0)
    argparser.add_argument('-s', '--size', default=1000)
    argparser.add_argument('-b', '--bins', default=100)
    argparser.add_argument('--loc1', default=25.0)
    argparser.add_argument('--loc2', default=75.0)
    argparser.add_argument('--scale1', default=20.0)
    argparser.add_argument('--scale2', default=20.0)
    argparser.add_argument('--size1', default=500)
    argparser.add_argument('--size2', default=500)
    return argparser.parse_args()

if __name__ == "__main__":
    args = get_args()

    number = int(args.number)
    out = args.out
    zerofill = args.zerofill

    if args.type in ['1', 'both']:
        loc = float(args.loc)
        scale = float(args.scale)
        size = int(args.size)
        bins = int(args.bins)
        suffix = args.format
        generate_graphs(is_normal_distribution=True,
            out=out,
            zerofill=zerofill,
            number=number,
            loc=loc, scale=scale, size=size,
            bins=bins, suffix=suffix)
    if args.type in ['2', 'both']:
        loc1 = float(args.loc1)
        scale1 = float(args.scale1)
        size1 = int(args.size1)
        loc2 = float(args.loc2)
        scale2 = float(args.scale2)
        size2 = int(args.size2)
        bins = int(args.bins)
        suffix = args.format    
        generate_graphs(is_normal_distribution=False,
            number=number,
            out=out,
            zerofill=zerofill,
            loc1=loc1, scale1=scale1, size1=size1,
            loc2=loc2, scale2=scale2, size2=size2,
            bins=bins, suffix=suffix)
