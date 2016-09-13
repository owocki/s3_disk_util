import boto3
from datetime import datetime, timedelta

in_memory_cache = {}

def cloudwatch_bucket_size(bucket_name):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/S3",
        MetricName="BucketSizeBytes",
        Dimensions=[
            {
                "Name": "BucketName",
                "Value": bucket_name
            },
            {
                "Name": "StorageType",
                "Value": "StandardStorage"
            }
        ],
        StartTime=datetime.now() - timedelta(days=1),
        EndTime=datetime.now(),
        Period=86400,
        Statistics=['Average']
    )
    datapoints = response['Datapoints']
    if len(datapoints) == 0:
        raise Exception('CloudWatch is not enabled.  Do you have the right region in your AWS config?')
    return response['Datapoints'][0]['Average']


def formatted_size(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def print_sizes_by_dir(bucket, _dir='/', target_depth=1, current_depth=0):

    # recursive bounds checking
    if current_depth > target_depth:
        return

    # setup
    prefix = "".join(['-' for i in range(0,current_depth)])

    # get size of files in this dir
    total_size = 0
    if _dir == '/':
        object_summary_iterator = bucket.objects.all()
    else:
        object_summary_iterator = bucket.objects.filter(Prefix=_dir).all()
    for obj in object_summary_iterator:
        path = obj.key
        total_size += obj.size

    # print out size
    hr_size = formatted_size(total_size)
    print(" {} {} : {}".format(prefix, _dir, hr_size))


    # iterate through next level dirs
    if _dir == '/':
        result = bucket.meta.client.list_objects(Bucket=bucket.name, Delimiter="/")
    else:
        result = bucket.meta.client.list_objects(Bucket=bucket.name, Delimiter="/", Prefix=_dir)
    dirs = result.get('CommonPrefixes')
    if dirs is not None:
        for o in dirs:
            dir_name = o.get('Prefix')

            # recursivly traverse this dir
            print_sizes_by_dir(bucket,dir_name, target_depth, current_depth+1)