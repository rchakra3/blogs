#!/usr/local/bin/python3

import shutil
import argparse
from azure.storage.blob import BlockBlobService


def zip_dir(src_path, zip_file_name='op'):
    shutil.make_archive(zip_file_name, 'zip', src_path)


def get_storage_conn(account_name, account_key):
    block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key)
    return block_blob_service

def create_container(block_storage, container_name, fail_if_exists=False):
    block_storage.create_container(container_name, fail_on_exist=fail_if_exists)

def zip_and_upload(src_file, account_name, account_key, container_name='buildartifacts', dest_file_name='op'):
    print("Creating zip file..")
    zip_dir(src_file, dest_file_name)
    print("Connecting to blob storage..")
    block_storage = get_storage_conn(account_name, account_key)
    print("Creating container")
    create_container(block_storage, container_name)
    print("Uploading file:" + dest_file_name + '.zip')
    block_storage.create_blob_from_path(container_name, dest_file_name + '.zip', dest_file_name + '.zip')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Zip and upload file to blob storage')
    parser.add_argument('-p', '--path', dest='path', help='path to directory you want to zip')
    parser.add_argument('-o', '--out', dest='out', help='name of output file', default='op')
    parser.add_argument('-n', '--account', dest='account_name', help='name of the storage account')
    parser.add_argument('-c', '--container', dest='container_name', help='name of storage container', default='buildartifacts')
    parser.add_argument('-k', '--key', dest='account_key', help='storage account key')
    args = parser.parse_args()
    
    if (args.account_name == None):
        args.account_name = os.environ['AZURE_STORAGE_ACCOUNT_NAME']
    
    if (args.account_key == None):
        args.account_key = os.environ['AZURE_STORAGE_ACCOUNT_KEY']

    zip_and_upload(args.path, args.account_name, args.account_key, args.container_name, args.out)

     


