import os
from subprocess import check_output
from tempfile import mkstemp
import sys

import boto3
import requests

s3 = boto3.client('s3')

S3_BUCKET = os.environ.get('AIRTABLE_BUCKET')
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API')
API_ENDPOINT = os.environ.get('AIRTABLE_API_ENDPOINT')


def _request(method, table, path, **kwargs):
    """Make a generic request with the Airtable API"""
    headers = {'Authorization': 'Bearer ' + AIRTABLE_API_KEY}
    url = API_ENDPOINT + table + path

    response = requests.request(method.upper(), url, headers=headers, **kwargs)
    response.raise_for_status()
    content = response.json()
    return content


def get_sample(sample_id):
    """Retrieve Samples record from Airtable API"""
    params = {
        'filterByFormula': '{Name} = "%s"' % sample_id,
    }
    records = _request('get', 'Samples', '/', params=params)['records']
    return records[0]


def update_sample(key, fields):
    """Update Samples record on Airtable"""
    new_record = {'fields': fields}
    return _request('patch', 'Samples', '/' + key, json=new_record)


def get_sequence_count(inpath):
    """Use samtools stats locally to get sequence count"""
    out = check_output('samtools stats {}'.format(inpath), shell=True)

    # Dig out the 'raw total sequences line' and return
    lines = [line.split('\t') for line in out.decode().split('\n')]
    for line in lines:
        if len(line) < 3:
            continue
        if line[1].startswith('raw total sequences'):
            return int(line[2])
    raise Exception("Can't find raw sequences")


def run(sample_id):
    """Run the pipeline for a given sample ID"""
    # Get sample record
    sample = get_sample(sample_id)

    # Download data to temp file
    _, tmp_in = mkstemp(suffix='.bam')
    s3.download_file(
        S3_BUCKET, 
        sample['fields']['BAM (S3 key)'], 
        tmp_in)

    # Run samtools on the temp file and get the output filepath
    seq_count = get_sequence_count(tmp_in)

    # Update Airtable by building object containing only fields that changed
    update_sample(sample['id'], {'Total reads': seq_count})


if __name__ == '__main__':
    run(sys.argv[1])