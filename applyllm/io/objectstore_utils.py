import boto3
from dataclasses import dataclass
from operator import attrgetter
from io import BytesIO
#from boto3.resources.factory.s3 import ServiceResource
from pypdf import PdfReader


@dataclass
class S3AccessConf():
    """
    Examples:
        s3_conf = S3AccessConf(
            bucket_name = "xxx",
            access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
            secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'),
            endpoint = os.environ.get('S3_ENDPOINT'),
            verify_host = True
        )    
    """
    access_key_id: str
    secret_access_key: str
    endpoint: str
    bucket_name: str
    verify_host: bool = True
    
    
class S3BucketHelper():
    # more about client caching
    def __init__(self, conf: S3AccessConf, file_prefix: str=""):
        """
        Args:
            file_prefix: s3 bucket objects key prefix used to filter the object
          
        Examples:
            S3BucketHelper(S3BucketConfig())
        """
        self.conf = conf      
        # session is the resource which can be passed around
        # https://github.com/boto/boto3/issues/3197#issuecomment-1180516179
        self.session = boto3.session.Session(
            aws_access_key_id = self.conf.access_key_id,
            aws_secret_access_key = self.conf.secret_access_key
        )
        self.file_prefix = file_prefix
 
    def _get_s3_resource(self):
        # resource is a s3 endpoint 
        s3 = self.session.resource('s3', endpoint_url = self.conf.endpoint, verify=self.conf.verify_host)
        return s3
             
    def get_object_keys(self, limit_count: int=-1, input_attr_key = "key") -> map:
        """
        Return:
            map generator object
        """
        # bucket_items = []
        s3 = self._get_s3_resource()
        bucket = s3.Bucket(self.conf.bucket_name)
        # for obj in bucket.objects.all():
        
        # Filter: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/collections.html#filtering
        
        # https://stackoverflow.com/questions/45477181/apply-map-over-property-in-python
        # map object https://realpython.com/python-map-function/
        if limit_count < 0:
            # use attrgetter(input_attr_key) to filter object streams and transform the object steam to a stream of the obj.input_attr_key
            bucket_items_map = map(attrgetter(input_attr_key), 
                    bucket.objects.filter(Prefix=self.file_prefix)
                   )
        else:
            bucket_items_map = map(attrgetter(input_attr_key), 
                    bucket.objects.filter(Prefix=self.file_prefix).limit(limit_count)
                   )
        return bucket_items_map
    
    def transform_objects(self, s3_keys: map, bytesio_transformer: callable, s3_body_key = "Body", output_id_key: str = "name", output_content_key: str = "bytesio") -> map:
        """
        transforms the selected the s3 object with a given transformer
        """
        # callable https://realpython.com/python-callable-instances/
        s3 = self._get_s3_resource()
        
        bytesio_map = map(lambda x: {
            output_id_key : x,
            output_content_key : BytesIO(s3.Object(self.conf.bucket_name, x).get()[s3_body_key].read())
        }, s3_keys)
        
        return map(bytesio_transformer, bytesio_map)
       
    def upload_objects(self, data: map, key_mutater: callable = lambda x:x, input_id_key:str = "name", input_body_key: str = "content") -> map:
        s3 = self._get_s3_resource()
        bucket = s3.Bucket(self.conf.bucket_name)
        
        return map(lambda x:
            bucket.put_object(Key=key_mutater(x.get(input_id_key)), Body=x.get(input_body_key))
            ,data)


class S3PdfObjHelper(S3BucketHelper):
        """helper class for S3 PDF object specificly
        """
        class DataContract:
            name = "name"
            # reader = "reader"
            content = "content"
            pages = "pages"
            max_token_per_seg = 350
            bytesio = "bytesio"
            key_lead = "trans2en"
            key_origin_pattern = "pdf"
            key_new_pattern = "txt"
           
        def __init__(self, conf: S3AccessConf, file_prefix: str=""):
            super().__init__(conf, file_prefix)
                   
        @classmethod
        def pdf_reader_transformer(clz, input_dict: dict) -> dict:
            """
            transforms a byte stream data sequence to a PdfReader stream sequence
            """
            return {
                clz.DataContract.name : input_dict.get(clz.DataContract.name),
                clz.DataContract.content : PdfReader(input_dict.get(clz.DataContract.bytesio))
            }
        
        @classmethod
        def read_pages_transformer(clz, input_dict: dict) -> dict:
            """
            transforms a RdfReader stream sequence to a plain text stream sequence
            """
            return {
                clz.DataContract.name: input_dict.get(clz.DataContract.name),
                clz.DataContract.content: "".join([page.extract_text() for page in input_dict.get(clz.DataContract.content).pages])
            }
        
        @classmethod
        def segment_pages_transformer(clz, input_dict: dict) -> dict:
            """
            transforms a plain text stream sequence to 
            a segmented plain text stream sequence.
            """
            #  https://stackoverflow.com/questions/13673060/split-string-into-strings-by-length
            s = input_dict.get(clz.DataContract.content) # input string
            w = clz.DataContract.max_token_per_seg            
            return {
                clz.DataContract.name: input_dict.get(clz.DataContract.name),
                clz.DataContract.content: [s[i:i + w] for i in range(0, len(s), w)]
            }
        
        @classmethod
        def custom_pages_transformer_factory(clz, segment_transformer: callable) -> dict:
            """
            a factory function 
            Args:
                segment_transformer: a customer transformer function
                
            Returns:
                a transformer function to tranformer a stream of segmented pages
                using the input pages_transformer
            """
            def inner_func(input_dict: dict):
                segment_output = []
                # loop throught the page segments
                for segment in input_dict.get(clz.DataContract.content):
                    # apply the custom segment_transformer
                    segment_output.append(segment_transformer(segment))
                return {
                    clz.DataContract.name: input_dict.get(clz.DataContract.name),
                    clz.DataContract.content: ''.join(segment_output)
                }
            return inner_func
                 
        @classmethod
        def s3_key_mutater(clz, old_key: str) -> str:
            return f"{clz.DataContract.key_lead}/{old_key.replace(clz.DataContract.key_origin_pattern, clz.DataContract.key_new_pattern)}"
        