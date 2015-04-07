import json
import zipfile
import os
import shutil
import sys

from pprint import pprint

class assembly:
	all_config_filename = "jarassemb.json"
	all_config_jar_dir = "src/jar"
	all_config_java_dir = "src/java"
	all_config_class_dir = "src/class"
	config_data = None
	jobs = None

	def initial_config(self):
		with open(self.all_config_filename) as data_file:
			self.config_data = json.load(data_file)
			self.jobs = self.config_data['jobs']

		# pprint(self.config_data)		

	def assemble_sources(self, job):
		'''assemble sources to classes'''
		target_dir = os.path.join("classes", job['job_name'] + "-" + job['archieve_version'] )
		if os.path.isdir(target_dir):
			shutil.rmtree(target_dir)
			print ('Old target folder removed.')	
		
		# self.__compile_java( job["filesets"]["java"], target_dir )
		self.__distribute_class( self.all_config_class_dir, job["filesets"]["class"], target_dir )
		self.__compress_jar_and_distribute_class( job["filesets"]["jar"], target_dir )

	def build_jar(self, job):
		'''build jar from classes/job_name'''
		class_path = os.path.join("classes", job['archieve_name'] + "-" + job['archieve_version'])
		jar_name = os.path.join("output", job['archieve_name'] + "-" + job['archieve_version'] + ".jar")
		
		zf = zipfile.ZipFile(jar_name, "w")

		for dirpath,dirs,files in os.walk(class_path):
			for f in files:
				fn = os.path.join(dirpath, f)
				zf.write(fn, fn.replace(class_path, ""))
				
		zf.close()

	# future work 	
	# def __compile_java(self, filesets, target):
	# 	print ('Function __compile_java')

	# 	try:
	# 		for file in filesets:
	# 			base_directory = os.path.join(self.all_config_java_dir, file['base_directory'])
	# 			print ('base_directory = ' + base_directory)

	# 			try:


	# 			except Exception as e:
	# 				print (str(e))
		
	# 	except:
	# 		print ('Failed in __compile_java')

	def __distribute_class(self, class_dir, filesets, target):
		print ('Function __distribute_class')
		try :
			for file in filesets:
				old_base_directory = file['base_directory']
				base_directory = os.path.join(class_dir, file['base_directory'])
				print ('base_directory = ' + base_directory)

				try: # user defined output directory
					output_directory = os.path.join(target, file['output_directory'])
					print ('User defined output_directory in config.')

					if os.path.isdir(base_directory):
						if not os.path.exists(output_directory):
							os.makedirs(output_directory)

						shutil.rmtree(output_directory)
						shutil.copytree(base_directory, output_directory)

					else: # file
						if '.class' in os.path.basename(output_directory):
							if not os.path.exists( os.path.dirname(output_directory) ):
								os.makedirs(os.path.dirname(output_directory))
								shutil.copyfile(base_directory, output_directory)
						else:
							if not os.path.exists(output_directory):
								os.makedirs(output_directory)
								shutil.copy(base_directory, output_directory)
				except Exception as e:
					print ('No output_directory in config.')
					print (str(e))

					if os.path.isdir(base_directory):
						if not os.path.exists(os.path.join(target, old_base_directory)):
							os.makedirs(os.path.join(target, old_base_directory))

						shutil.rmtree(os.path.join(target, old_base_directory))
						shutil.copytree(base_directory, os.path.join(target, old_base_directory))
					else: # file
						if not os.path.exists( os.path.join(target, os.path.dirname(old_base_directory)) ):
							os.makedirs(os.path.join(target, os.path.dirname(old_base_directory)))

						shutil.copyfile(base_directory, os.path.join(target, old_base_directory))

		except Exception as e:
			print ('Failed in __distribute_class')
			print (str(e))

	def __compress_jar_and_distribute_class(self, jars, target):
		print ('Function __compress_jar_and_distribute_class')

		try:
			for jar in jars:
				print ('jar_name = ' + jar['jar_name'])
				print (self.all_config_jar_dir)
				fs = open(os.path.join(self.all_config_jar_dir, jar['jar_name']+'.jar'), 'rb')
				zf = zipfile.ZipFile(fs)
				jar_output_dir = os.path.join(self.all_config_jar_dir, jar['jar_name'])
				if os.path.isdir(jar_output_dir):
					shutil.rmtree(jar_output_dir)
					print ('Old extracted folder removed.')	
				zf.extractall(jar_output_dir)
				fs.close()
				self.__distribute_class(jar_output_dir, jar["filesets"], target)
		except Exception as e:
			print ('Failed in __compress_jar_and_distribute_class')
			print (str(e))

def main(argv):
	e = assembly()
	
	if len(argv) == 2:
		print ('User defined class path and jar path')
		e.all_config_jar_dir = argv[1]
		e.all_config_class_dir = argv[0]
	elif len(argv) == 1:
		print ('User defined class path')
		e.all_config_class_dir = argv[0]
	elif len(argv) == 0:
		print ('Default mode')
	else:
		print ('Wrong number of arguments')
		return 
	
	e.initial_config()
	if e.jobs != None:
		e.assemble_sources( e.jobs[0] )
		e.build_jar( e.jobs[0] )

if __name__ == '__main__':
	main(sys.argv[1:])

