# s3_disk_util

* _What_ -- A tool that allows a user to visualize which buckets (and parts of buckets) are using the most data storage.
* _Why_ -- Because I'm trying to pare down my S3 bill, and the S3 control panels (even CloudWatch) do not really provide anything similar.
* _Inspiration_ -- This script is meant to be like the `du` tool for linux, except for inspecting the disk usage of s3 buckets.  
* _How_ -- It will traverse s3 buckets and provide high level disk usage information to stdout.

# Usage

```bash
% python3 du.py --help
usage: du.py [-h] [-b BUCKET] [-p PROFILE] [-d DEPTH] [-di DIR]

This script is meant to be like the `du` tool for linux, except for inspecting
the disk usage of s3 buckets. It will traverse s3 buckets and provide high
level disk usage information to stdout.

optional arguments:
  -h, --help            show this help message and exit
  -b BUCKET, --bucket BUCKET
                        Bucket to examine (ex: 'com.owocki.assets')
  -p PROFILE, --profile PROFILE
                        AWS credentials profile name (default: 'default')
  -d DEPTH, --depth DEPTH
                        Depth to examine bucket (ex: 4)
  -di DIR, --dir DIR    Directory to examine (ex: 'logs/')
  ```

## Example

```bash
% python3 du.py --depth=1 --bucket=BUCKETNAME --profile=mytestaccount
BUCKETNAME
(Cloudwatch bucket size estimate: 22.7GiB)
  / : 22.7GiB
 - DIR1/ : 22.6GiB
 - DIR2/ : 452.6KiB
 - DIR3/ : 1.6MiB
 - DIR4/ : 119.0MiB
 - DIR5/ : 0.0B

% python3 du.py --depth=2 --bucket=BUCKETNAME
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

1. Create an AWS IAM user account at (https://console.aws.amazon.com/iam/home).
    * Make sure your user has `AmazonS3FullAccess` and `CloudWatchReadOnlyAccess` policies.
2. Use your existing `~/.aws/credentials` file and profile names or create a config file that looks like this:
```bash
% cat ~/.aws/credentials

[default]
aws_access_key_id = ACCESS_KEY_GOES_HERE
aws_secret_access_key = SECRET_KEY_GOES_HERE
region=REGION
```
3. Clone this repo.
4. Install python3 (if needed) and boto3 (if needed).
    * To install python3, instructions differ depending upon your OS. Using Homebrew is probably the easiest (`brew install python3`), or here are some instructions for [Mac OS X](http://www.marinamele.com/2014/07/install-python3-on-mac-os-x-and-use-virtualenv-and-virtualenvwrapper.html)
    * To install boto3, `pip install -r requirements.txt`
5. Run `du.py` with the usage described above.

# What else

This script can run a little slow on larger buckets.  Thats okay; This is a limitation inherent to the way this information is provided via AWS APIs.  Pipe `du.py`'s' output to a file (perhaps inside of a `screen` or `tmux`) and come back later.


<!-- Google Analytics -->
<img src='https://ga-beacon.appspot.com/UA-1014419-15/owocki/s3_disk_util' style='width:1px; height:1px;' >
