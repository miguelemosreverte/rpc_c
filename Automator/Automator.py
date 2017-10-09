import os
import sys
import yaml
import argparse
import shutil


class Automator:

	def __init__(self, filepath):
		self.basepath, self.filename = os.path.split(filepath)
		self.filepath = filepath
		self.filename_without_extension = os.path.splitext(self.filename)[0]

		self.own_script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
		self.working_directory = os.getcwd()

		# Read YAML file
		with open(self.own_script_path + "/data_injection.yaml", 'r') as stream:
			data_loaded = yaml.load(stream)
			self.rpcgen = data_loaded["rpcgen"]
			self.cunit = data_loaded["cunit"]
			self.cleanup = data_loaded["cleanup"]


	def runAutomatedTasks(self):
		self.run_cleanup()
		self.RPCGEN()
		self.CUnit()

	def RPCGEN(self):
		os.chdir(self.basepath)
		self.rpcgen = map(lambda x: x.replace("filename_without_extension", self.filename_without_extension), self.rpcgen)
		self.rpcgen = map(lambda x: x.replace("filename", self.filename), self.rpcgen)
		for command in self.rpcgen:
			os.system(command)
		os.chdir(self.working_directory)

	def CUnit(self):
		template = ""
		CUnit_dir = self.own_script_path + "/CUnit__TestGenerator/"

		#read template content
		with open (CUnit_dir + "/CUnitTests.c", 'r') as f:
			template =  f.read()

		#add tests
		tests = [self.cunit["tests_codeblocks"][test_name] for test_name in self.cunit["tests_codeblocks"]]
		for test_name in self.cunit["test_files"]:
			with open (self.basepath + "/" + self.cunit["test_files"][test_name], 'r') as f:
				tests.append(f.read())
		#inject them
		template = template.split(self.cunit["inject_tests_here"])
		template = template[0] +  "\n".join(tests) + template[1]

		#add asserts
		template = template.split(self.cunit["insert_assertions_here"])
		assertion_template =  template[1].split("\n")[1]
		test_names = dict(self.cunit["tests_codeblocks"].items() +  self.cunit["test_files"].items())
		assertions = [assertion_template.replace("testname", test_name) for test_name in test_names]
		template = template[0] +  " || \n".join(assertions) + template[1].replace(assertion_template,"")

		#copy own CUnit template folder to new CUnit folder
		newCUnit_dir = self.basepath + "/CUnit/"
		if os.path.exists(newCUnit_dir): shutil.rmtree(newCUnit_dir)
		shutil.copytree(CUnit_dir, newCUnit_dir)
		#add modified CUnitTests.c to the new CUnit folder
		with open (newCUnit_dir + "/CUnitTests.c", 'w') as f:
			f.write(template)

	def run_cleanup(self):
		suffixes = self.cleanup["suffixes"]
		for item in os.listdir(self.basepath):
		    for suffix in suffixes:
				if item.endswith(suffix):
					os.remove(os.path.join(self.basepath, item))


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('filepath')
	args = parser.parse_args()

	MyAutomator = Automator(args.filepath)


	basepath, filename = os.path.split(args.filepath)
	if not os.path.exists(args.filepath):
		print "Pick an existing file"
	else:
		MyAutomator.runAutomatedTasks()
