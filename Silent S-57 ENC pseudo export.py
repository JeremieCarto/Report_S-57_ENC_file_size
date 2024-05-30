# Runs ExportHPDS57Product using create-test-version and captures either the full path to the file or the error message.
# J.Robichaud
# 19-04-2024
# Python version 3.11

def execute_process(sources, progress):
	
	import os
	import subprocess
	from subprocess import CREATE_NO_WINDOW
	
	#Get the HPD URI
	hpd_uri = sources.get('hpd_uri')
	
	#Set the hardcoded destination folder. This is never exposed to users. All files and folders will be deleted after use, leaving no trace.
	destinationfolder = "C:\\Users\\" + os.getenv('username') + "\\AppData\\Roaming\\CARIS\\HPD"

	#Export silently a test version. Hide the console window.
	silent_export = subprocess.run(["C:\\Program Files\\CARIS\\HPD\\5.0\\Bin\\carisbatch.exe", "--run", "ExportHPDS57Product", "--create-test-version", "--destination-folder", destinationfolder, hpd_uri], text=True, creationflags=CREATE_NO_WINDOW, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
	#Change subprocess output to string
	output = str(silent_export)

	#Check if product was exported
	if (output.find("Product exported") != -1): # -1 is returned if string is not found
		#Capture the path from output
		sources['exported_file'] = output[output.index("Product exported") + 20:output.index("\\nThe file is also")].replace("\\\\", "\\")
		sources['error'] = False
	else:
		#Capture the error message
		sources['error_message'] = "\n" + str(silent_export.stderr)
		sources['error'] = True