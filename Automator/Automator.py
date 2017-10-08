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
			self.ctests = data_loaded["ctests"]

	def RPCGEN(self):
		os.chdir(self.basepath)
		self.rpcgen = map(lambda x: x.replace("filename_without_extension", self.filename_without_extension), self.rpcgen)
		self.rpcgen = map(lambda x: x.replace("filename", self.filename), self.rpcgen)
		for command in self.rpcgen:
			os.system(command)
		os.chdir(self.working_directory)

	def CUnit(self):
		content = ""
		CUnit_dir = self.own_script_path + "/CUnit__TestGenerator/"
		with open (CUnit_dir + "/CUnitTests.c", 'r') as f:
			content =  f.read()

		#add tests
		tests = [self.ctests["tests"][test_name] for test_name in self.ctests["tests"]]
		content = content.split(self.ctests["inject_tests_here"])
		content = content[0] +  "\n".join(tests) + content[1]

		#add asserts
		content = content.split(self.ctests["insert_assertions_here"])
		assertion_template =  content[1].split("\n")[1]
		assertions = [assertion_template.replace("testname", test_name) for test_name in self.ctests["tests"]]
		content = content[0] +  " || \n".join(assertions) + content[1].replace(assertion_template,"")

		#copy own CUnit template folder to new CUnit folder
		newCUnit_dir = self.basepath + "/CUnit/"
		shutil.copytree(CUnit_dir, newCUnit_dir)
		#add modified CUnitTests.c to the new CUnit folder
		with open (newCUnit_dir + "/CUnitTests.c", 'w') as f:
			f.write(content)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('filepath')
	args = parser.parse_args()

	def runAutomatedTask():
		MyAutomator = Automator(args.filepath)
		MyAutomator.RPCGEN()
		MyAutomator.CUnit()

	basepath, filename = os.path.split(args.filepath)
	if not os.path.exists(args.filepath):
		print "Pick an existing file"
	elif os.path.exists(basepath + "/makefile"):
		print "Already ran automated task. Do you want to overwrite it? Y/N"
		if raw_input() in ["Y","y"]:
			content = ""
			with open (args.filepath, 'r') as f: content = f.read()
			shutil.rmtree(basepath)
			os.mkdir(basepath)
			with open (args.filepath, 'w') as f: f.write(content)
			runAutomatedTask()
	else:
		runAutomatedTask()
