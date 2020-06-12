import boto3
import os
import subprocess
import configparser
import pymailer
import tarfile
from hdfs.ext.kerberos import KerberosClient
from logger_setting import *
from datetime import datetime, date, timedelta

py_logger=logging.getLogger('py_logger')

try:
    #Your certificate location
    os.environ["REQUESTS_CA_BUNDLE"]="/etc/security/rootCA.pem"

    config_path = '/edgenode/s3/upload/s3_config.conf'
    configuration_file = configparser.ConfigParser()
    config = configuration_file.read_file(open(config_path))

    access_key_id = configuration_file.get('config', 'aws_access_key_id')
    secret_access_key = configuration_file.get('config', 'aws_secret_access_key')

    s3_folder_name = configuration_file.get('config', 's3_folder_name')
    bucket_name = configuration_file.get('config', 'bucket_name')
    hive_script_name = configuration_file.get('config', 'hive_script_name')
    hdfs_url = configuration_file.get('config', 'hdfs_url')
    source_directory = configuration_file.get('config', 'source_directory')
    log_file_path = configuration_file.get('config', 'log_file_path')
    
    hive_db_a = configuration_file.get('config', 'hive_db_a')
    hive_db_b = configuration_file.get('config', 'hive_db_b')

    session = boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )

    py_logger.info("hive execution started")

    file_list = subprocess.check_output([hive_script_name,hive_db_a,hive_db_b])
    file_list_arr = file_list.split(' ')

    py_logger.info("hive execution completed")

    client = KerberosClient(hdfs_url)

    s3 = session.client('s3',use_ssl=False, verify=False)
    counter = 0

    for file_path in file_list_arr:

        file_path = source_directory + file_path

        status = client.status(file_path, strict=False)

        if bool(status):
            file_name = os.path.basename(file_path)
            key_name = s3_folder_name + file_name

            with client.read(file_path) as f:
                s3.upload_fileobj(f, bucket_name, key_name)

            client.delete(file_path, recursive=False, skip_trash=True)
            counter = counter + 1
            py_logger.info("File: " + file_path + " moved to s3 bucket")
        
    py_logger.info("S3 script execution completed. No.of Files moved: " + str(counter))

	#Compresses the log files which are greater than 30 days
    today = date.today()
    current_day = datetime.now().strftime('%d')
    log_directory = log_file_path.rpartition('/')[0] + log_file_path.rpartition('/')[1]
    tarFileName = log_directory + today.strftime("%d-%m-%Y") + '.tar.gz'
	
    if current_day == "30":
        # writing files to a compressed file
        with tarfile.open(tarFileName, "w:gz") as tar:
            # writing each file one by one
            for folderName, subfolders, filenames in os.walk(log_directory):
                for filename in filenames:
                    # create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)

                    to_date = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
                    modTimesinceEpoc = os.path.getmtime(filePath)
                    modificationTime = datetime.fromtimestamp(modTimesinceEpoc).strftime('%Y-%m-%d')

                    if (modificationTime <= to_date):
                        # add the file to tar.gz
                        tar.add(filePath)
                        # remove the file from directory
                        os.remove(filePath)

except Exception as e:
    py_logger.error(e)
    pymailer.send_mail(str(e))

