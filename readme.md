# s3_disk_util

* _What_ -- A tool that allows a user to visualize which buckets (and parts of buckets) are using the most data storage.
* _Why_ -- The S3 control panels (even CloudWatch) do not really provide anything similar.
* _Inspiration_ -- This script is meant to be like the `du` tool for linux, except for inspecting the disk usage of s3 buckets.  
* _How_ -- It will traverse s3 buckets and provide high level disk usage information to stdout.

# Usage

```
kevinowocki@local /Users/kevinowocki/Desktop/s3_disk_util~ % python3 du.py --help
usage: du.py [-h] [-b BUCKET] [-d DEPTH] [-di DIR]

This script is meant to be like the `du` tool for linux, except for inspecting
the disk usage of s3 buckets. It will traverse s3 buckets and provide high
level disk usage information to stdout.

optional arguments:
  -h, --help            show this help message and exit
  -b BUCKET, --bucket BUCKET
                        Bucket to examine (ex: 'com.owocki.assets')
  -d DEPTH, --depth DEPTH
                        Depth to examine bucket (ex: 4)
  -di DIR, --dir DIR    Directory to examine (ex: 'logs/')
  ```

## Example

  ```
  kevinowocki@local /Users/kevinowocki/Desktop/s3_disk_utils~ % python3 du.py --depth=1 --bucket=BUCKETNAME
BUCKETNAME
(Cloudwatch bucket size estimate: 22.7GiB)
  / : 22.7GiB
 - DIR1/ : 22.6GiB
 - DIR2/ : 452.6KiB
 - DIR3/ : 1.6MiB
 - DIR4/ : 119.0MiB
 - DIR5/ : 0.0B

kevinowocki@local /Users/kevinowocki/Desktop/s3_disk_util~ % python3 du.py --depth=2 --bucket=BUCKETNAME
BUCKETNAME
(Cloudwatch bucket size estimate: 22.7GiB)
  / : 22.7GiB
 - DIR1/ : 22.6GiB
 -- DIR1/SUBDIR1/ : 31.1MiB
 -- DIR1/SUBDIR2/ : 12.7GiB
 -- DIR1/SUBDIR3/ : 0.0B
 -- DIR1/SUBDIR4/ : 9.9GiB
 - DIR2/ : 452.6KiB
 -- DIR2/SUBDIR1/ : 429.5KiB
 - DIR3/ : 1.6MiB
 -- DIR3/SUBDIR1/ : 254.4KiB
 - DIR4/ : 119.0MiB
 - DIR5/ : 0.0B

 ```

# Setup

1. Create a AWS IAM user at https://console.aws.amazon.com/iam/home.
    * Make sure your user has `AmazonS3FullAccess` and `CloudWatchReadOnlyAccess` policies.
2. Create a config file that looks like this:
```
kevinowocki@local /Users/kevinowocki/Desktop/s3_disk_utils~ % cat ~/.aws/credentials
[default]
aws_access_key_id = AKIAJCK54GNLN5DGAUGQ
aws_secret_access_key = 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
region=us-west-2
```
3. Clone this repo.
4. Install python3 (if needed) and boto3 (if needed).
    * To instally python3, instructions different depending upon your OS.  Here are some instructions for [Mac OS X](http://www.marinamele.com/2014/07/install-python3-on-mac-os-x-and-use-virtualenv-and-virtualenvwrapper.html)
    * To install boto3, `pip install -r requirements.txt`
5. Run `du.py` with the usage described above.

# What else

This script can run a little slow on larger buckets.  Thats okay; This is a limitation inherent to the way this information is provided via AWS APIs.  Pipe `du.py`'s' output to a file (perhaps inside of a `screen` or `tmux`) and come back later.
