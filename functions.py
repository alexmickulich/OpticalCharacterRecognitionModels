__author__ = 'Artgor'
from codecs import open
import os
import uuid
import boto3
from boto.s3.key import Key
from boto.s3.connection import S3Connection


class Model(object):
	def __init__(self):
		#self.model = joblib.load()
		self.nothing = 0

	def save_image(self, drawn_digit, image):
		filename = 'digit' + str(drawn_digit) + '__' + str(uuid.uuid1()) + '.jpg'
		with open('tmp/' + filename, 'wb') as f:
			f.write(image)
			
		print('Image written')
		
		REGION_HOST = 's3-external-1.amazonaws.com'
		conn = S3Connection(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'], host=REGION_HOST)
		bucket = conn.get_bucket('rootdigit')
		
		k = Key(bucket)
		fn = 'tmp/' + filename
		k.key = filename
		k.set_contents_from_filename(fn)
		print('Done')

		return ('Image saved successfully with the name {0}'.format(filename))

	def download_image(self):
		s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
		for obj in s3.list_objects(Bucket=BUCKET)['Contents']:
			filename = obj['Key']
			if 'digit' in filename:
				# The local directory must exist.
				localfilename = os.path.join('my_images/', filename)
				s3.download_file(BUCKET, filename, localfilename)
				return ('Images download successfuly')
			else:
				pass
