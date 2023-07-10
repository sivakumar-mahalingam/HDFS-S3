# HDFS <-> S3
This Python script allows you to easily upload and download files between Hadoop Distributed File System (HDFS) and Amazon Simple Storage Service (S3) using the AWS SDK for Python (Boto3).

## Prerequisites
Before running this script, make sure you have the following prerequisites:

- Python 3.x installed on your system.
- Boto3 library installed. You can install it by running the following command:
```
pip install boto3
```
- AWS credentials configured on your system. You can set up your AWS access key ID and secret access key using the AWS Command Line Interface (CLI) or by configuring the AWS credentials file manually.
## Usage

1. Clone this repository to your local machine.
    
2. Open the `s3_config.conf` file in a text editor.
    
3. Modify the following variables at the beginning of the script according to your requirements:
    
    - `AWS_ACCESS_KEY`: Your AWS access key ID.
    - `AWS_SECRET_KEY`: Your AWS secret access key.
    - `AWS_REGION`: The AWS region where your S3 bucket is located.
    - `S3_BUCKET_NAME`: The name of your S3 bucket.
    - `HDFS_URL`: The URL of your HDFS namenode.
    - `HDFS_USERNAME`: The username for HDFS authentication.
    - `HDFS_PATH`: The HDFS path of the file or directory you want to upload/download.
4. Save the modified script.
    
5. Open a terminal or command prompt and navigate to the directory where the script is located.
    
6. To upload a file or directory from HDFS to S3, run the following command:
```
python /HDFS-S3/Upload/s3_upload.py
```
7. To download a file or directory from S3 to HDFS, run the following command:
```
python /HDFS-S3/Download/s3_download.py.py
```
## Notes

- Make sure you have proper permissions and access to both the HDFS and S3 resources.
- The script uses the default encryption settings for S3 uploads/downloads. If you require specific encryption settings, modify the script accordingly.
- For large files or directories, the transfer may take some time to complete. Please be patient and wait for the script to finish.
## License

This script is licensed under the [MIT License](https://chat.openai.com/LICENSE). Feel free to modify and use it according to your needs.
