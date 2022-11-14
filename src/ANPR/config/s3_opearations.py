import os, sys, pickle
from src.ANPR import logging
from io import StringIO
from typing import List, Union
from src.ANPR.config.aws_connection import S3Client
from mypy_boto3_s3.service_resource import Bucket
from src.ANPR.exception import ANPRException
from keras.models import load_model
from botocore.exceptions import ClientError
from pandas import DataFrame,read_csv



class S3Operation:
    def __init__(self):
        s3_client = S3Client()
        self.s3_resource = s3_client.s3_resource
        self.s3_client = s3_client.s3_client
    
    @staticmethod
    def read_object(object_name: str, decode: bool = True, make_readable: bool = False) -> Union[StringIO, str]:
        """
        Method Name :   read_object
        Description :   This method reads the object_name object with kwargs

        Output      :   The column name is renamed
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered the read_object method of S3Operations class")

        try:
            func = (
                lambda: object_name.get()["Body"].read().decode()
                if decode is True
                else object_name.get()["Body"].read()
            )
            conv_func = lambda: StringIO(func()) if make_readable is True else func()
            logging.info("Exited the read_object method of S3Operations class")
            return conv_func()

        except Exception as e:
            raise ANPRException(e, sys) from e

    
    def get_bucket(self, bucket_name: str) -> Bucket:

        """
        Method Name :   get_bucket
        Description :   This method gets the bucket object based on the bucket_name
        
        Output      :   Bucket object is returned based on the bucket name
        """
        logging.info("Entered the get_bucket method of S3Operations class")
        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            logging.info("Exited the get_bucket method of S3Operations class")
            return bucket

        except Exception as e:
            raise ANPRException(e, sys) from e

    
    def download_file(self, bucket_name: str, output_file_path: str, key: str) -> None:

        """
        Method Name :   download_file
        Description :   This method downloads the file from the s3 bucket and saves the file in directory 
        
        Output      :   File is saved in local
        """
        logging.info("Entered the download_file method of S3Operation class")
        try:
            self.s3_resource.Bucket(bucket_name).download_file(key, output_file_path)
            logging.info("Exited the download_file method of S3Operation class")

        except Exception as e:
            raise ANPRException(e, sys) from e
    
    def load_model(
        self, model_name: str, bucket_name: str, model_dir: str = None
    ) -> object:

        """
        Method Name :   load_model
        Description :   This method loads the model_name from bucket_name bucket with kwargs
        
        Output      :   list of objects or object is returned based on filename
        """
        logging.info("Entered the load_model method of S3Operations class")

        try:
            func = (
                lambda: model_name
                if model_dir is None
                else model_dir + "/" + model_name
            )
            model_file = func()
            f_obj = self.get_file_object(model_file, bucket_name)
            model_obj = self.read_object(f_obj, decode=False)
            model = pickle.loads(model_obj)
            logging.info("Exited the load_model method of S3Operations class")
            return model

        except Exception as e:
            raise ANPRException(e, sys) from e

    
    def load_h5_model(self,bucket_name,object_file_name,local_file_name):
        try:
            self.download_file(bucket_name,local_file_name,object_file_name)

            model = load_model(local_file_name)

            return model
            
        except Exception as e:
            raise e 
        

    def get_image(self, bucket_name: str, prefix: str, total_number_of_images: int) -> List:

        """
        Method Name :   get_image
        Description :   This method gets the images from the mentioned prefix(folder name)
        
        Output      :   Bucket object is returned based on the bucket name and prefix
        """
        logging.info("Entered the get_image method of S3Operations class")
        try:
            my_bucket = self.s3_resource.Bucket(bucket_name)
            bucket_list = []
            for file in my_bucket.objects.filter(Prefix = prefix):
                file_name = file.key
                if file_name.find(".jpg") != -1:
                    bucket_list.append(file.key)
            
            logging.info("Exited the get_image method of S3Operations class")
            return bucket_list[0:total_number_of_images]

        except Exception as e:
            raise ANPRException(e, sys) from e

    
    def is_model_present(self, bucket_name: str, s3_model_key: str) -> bool:

        """
        Method Name :   is_model_present
        Description :   This method validates whether model is present in the s3 bucket or not.
        
        Output      :   True or False
        """
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [
                file_object
                for file_object in bucket.objects.filter(Prefix=s3_model_key)
            ]
            if len(file_objects) > 0:
                return True
            else:
                return False

        except Exception as e:
            raise ANPRException(e, sys) from e


    def get_file_object(
        self, filename: str, bucket_name: str
    ) -> Union[List[object], object]:
        """
        Method Name :   get_file_object
        Description :   This method gets the file object from bucket_name bucket based on filename 
        
        Output      :   list of objects or object is returned based on filename
        """
        logging.info("Entered the get_file_object method of S3Operations class")
        try:
            bucket = self.get_bucket(bucket_name)
            lst_objs = [object for object in bucket.objects.filter(Prefix=filename)]
            func = lambda x: x[0] if len(x) == 1 else x
            file_objs = func(lst_objs)
            logging.info("Exited the get_file_object method of S3Operations class")
            return file_objs

        except Exception as e:
            raise ANPRException(e, sys) from e

    
    def create_folder(self, folder_name: str, bucket_name: str) -> None:

        """
        Method Name :   create_folder
        Description :   This method creates a folder_name folder in bucket_name bucket
        
        Output      :   Folder is created in s3 bucket
        """
        logging.info("Entered the create_folder method of S3Operations class")

        try:
            self.s3_resource.Object(bucket_name, folder_name).load()

        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                folder_obj = folder_name + "/"
                self.s3_client.put_object(Bucket=bucket_name, Key=folder_obj)
            else:
                pass
            logging.info("Exited the create_folder method of S3Operations class")

    
    def upload_file(
        self,
        from_filename: str,
        to_filename: str,
        bucket_name: str,
        remove: bool = True,
    ) -> None:

        """
        Method Name :   upload_file
        Description :   This method uploads the from_filename file to bucket_name bucket with to_filename as bucket filename
        
        Output      :   Folder is created in s3 bucket
        """
        logging.info("Entered the upload_file method of S3Operations class")
        try:
            logging.info(
                f"Uploading {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )

            self.s3_resource.meta.client.upload_file(
                from_filename, bucket_name, to_filename
            )
            logging.info(
                f"Uploaded {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )

            if remove is True:
                os.remove(from_filename)
                logging.info(f"Remove is set to {remove}, deleted the file")
            else:
                logging.info(f"Remove is set to {remove}, not deleted the file")
            logging.info("Exited the upload_file method of S3Operations class")

        except Exception as e:
            raise ANPRException(e, sys) from e


    def upload_folder(self, folder_name: str, bucket_name: str) -> None:

        """
        Method Name :   upload_file
        Description :   This method uploads the from_filename file to bucket_name bucket with to_filename as bucket filename
        
        Output      :   Folder is created in s3 bucket
        """
        logging.info("Entered the upload_folder method of S3Operations class")
        try:
            lst = os.listdir(folder_name)
            for f in lst:
                local_f = os.path.join(folder_name, f)
                dest_f = f
                self.upload_file(local_f, dest_f, bucket_name, remove=False)
            logging.info("Exited the upload_folder method of S3Operations class")

        except Exception as e:
            raise ANPRException(e, sys) from e
        
    def upload_df_as_csv(
        self,
        data_frame: DataFrame,
        local_filename: str,
        bucket_filename: str,
        bucket_name: str,
    ) -> None:

        """
        Method Name :   upload_df_as_csv
        Description :   This method uploads the dataframe to bucket_filename csv file in bucket_name bucket 
        
        Output      :   Folder is created in s3 bucket
        """
        logging.info("Entered the upload_df_as_csv method of S3Operations class")
        try:
            data_frame.to_csv(local_filename, index=None, header=True)
            self.upload_file(local_filename, bucket_filename, bucket_name)
            logging.info("Exited the upload_df_as_csv method of S3Operations class")

        except Exception as e:
            raise ANPRException(e, sys) from e

    
    def get_df_from_object(self, object_: object) -> DataFrame:

        """
        Method Name :   get_df_from_object
        Description :   This method gets the dataframe from the object_name object 
        
        Output      :   Folder is created in s3 bucket
        """
        logging.info("Entered the get_df_from_object method of S3Operations class")

        try:
            content = self.read_object(object_, make_readable=True)
            df = read_csv(content, na_values="na")
            logging.info("Exited the get_df_from_object method of S3Operations class")
            return df

        except Exception as e:
            raise ANPRException(e, sys) from e

    def read_csv(self, filename: str, bucket_name: str) -> DataFrame:

        """
        Method Name :   get_df_from_object
        Description :   This method gets the dataframe from the object_name object 
        
        Output      :   Folder is created in s3 bucket
        """
        logging.info("Entered the read_csv method of S3Operations class")
        try:
            csv_obj = self.get_file_object(filename, bucket_name)
            df = self.get_df_from_object(csv_obj)
            logging.info("Exited the read_csv method of S3Operations class")
            return df

        except Exception as e:
            raise ANPRException(e, sys) from e


    def download_file(self, bucket_name: str, output_file_path: str, key: str) -> None:

        """
        Method Name :   download_file
        Description :   This method downloads the file from the s3 bucket and saves the file in directory 
        
        Output      :   File is saved in local
        """
        logging.info("Entered the download_file method of S3Operation class")
        try:
            self.s3_resource.Bucket(bucket_name).download_file(key, output_file_path)
            logging.info("Exited the download_file method of S3Operation class")

        except Exception as e:
            raise ANPRException(e, sys) from e


    def read_data_from_s3(self, bucket_filename: str, bucket_name: str, output_filepath: str) -> None:

        """
        Method Name :   read_data_from_s3
        Description :   This method downloads the file from the s3 bucket and saves the file in directory 
        
        Output      :   returns object.
        """
        logging.info("Entered the read_data_from_s3 method of S3Operation class")
        try:
            bucket = self.get_bucket(bucket_name)
            obj = bucket.download_file(Key=bucket_filename, Filename=output_filepath)
            logging.info("Exited the read_data_from_s3 method of S3Operation class")
            return obj
            
        except Exception as e:
            raise ANPRException(e, sys) from e
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            