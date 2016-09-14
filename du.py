#!/usr/bin/python3

import argparse
import boto3
from botocore.exceptions import NoCredentialsError, NoRegionError
from helpers import cloudwatch_bucket_size, formatted_size, print_sizes_by_dir
import sys

parser = argparse.ArgumentParser(description="This script is meant to be like the `du` tool for linux, except for inspecting the disk usage of s3 buckets.  It will traverse s3 buckets and provide high level disk usage information to stdout.")
parser.add_argument("-b", "--bucket", help="Bucket to examine (ex: 'com.owocki.assets')")
parser.add_argument("-d", "--depth", type=int, default=1, help="Depth to examine bucket (ex: 4)")
parser.add_argument("-di", "--dir", default='/', help="Directory to examine (ex: 'logs/')")

# setup
try:
    s3 = boto3.resource('s3',config=boto3.session.Config(signature_version='s3v4'))

    # args
    args = parser.parse_args()

    if not args.bucket:
        buckets = s3.buckets.all()
    else:
        buckets = [s3.Bucket(args.bucket)]

    target_depth = args.depth
    target_dir = args.dir


    # Print out bucket names
    for bucket in buckets:
        print(bucket.name)

        #get high level stats from cloudwatch
        try:
            cloudwatch_bucket_size_formatted = formatted_size(cloudwatch_bucket_size(bucket.name))
            print('(Cloudwatch bucket size estimate: {})'.format(cloudwatch_bucket_size_formatted))
        except Exception as e:
            print("Could not get cloudwatch stats: {}".format(e))

        # traverse dirs in s3 bucket
        print_sizes_by_dir(bucket, _dir=target_dir, target_depth=target_depth)

except NoCredentialsError:
    print("Unable to locate aws credentials.  Please make sure you have the following configuration file at '~/.aws/credentials': \n\n" + \
        "[default]\n" + \
        "aws_access_key_id = YOURACCESSKEY\n" + \
        "aws_secret_access_key = YOURSECRETKEY\n" + \
        "region=YOURREGION\n")
    exit(0)
    
