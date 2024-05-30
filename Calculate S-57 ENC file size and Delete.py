# Reports the size of an S-57 ENC file (either base cell or update), then deletes the file.
# J.Robichaud
# 19-04-2024
# Python version 3.11


def execute_process(sources, progress):
	import os
	import urllib.parse
	import shutil

	#Remove extra slashes from path
	exported_file = urllib.parse.unquote(sources.get('exported_file'))

	#Get the file size in bytes
	size = os.path.getsize(exported_file)
	
	#Look at the file extension to differentiate a base cell from an update and output file size
	fileextension = exported_file[exported_file.rfind(".") + len("."):]
	
	if fileextension == "000":
		type = "base cell"
		if size < 1024000: #if size smaller than 1000KB
			size = int(size/1024) #Size in bytes converted to KB
			sources['message'] =  "\n Information:  Upon export, the size of the " + type + " will be " + str(size) + " KB\n"
		else:
			size = round (size/1024/1024,2) #Size in bytes converted to MB, keep 2 decimals
			sources['message'] =  "\n Information:  Upon export, the size of the " + type + " will be " + str(size) + " MB\n"
	else:
		type = "Update"
		updatenumber = fileextension.lstrip("0") #Update number is the file extension without leading zeros
		size = round (size/1024,1) #Size in bytes  to KB, keep one decimal
		sources['message'] =  "\n Information:  Upon export, the size of " + type + " " + updatenumber + " will be " + str(size) + " KB\n"
	
	#Delete S-57 ENC folder
	datasetname_length = 8
	datasetname = exported_file[exported_file.rfind(".") - datasetname_length : exported_file.rfind(".")]
	shutil.rmtree(exported_file[:exported_file.find(datasetname) + datasetname_length])

