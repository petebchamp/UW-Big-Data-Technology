#Extract .csv files from .zip files
#using the ZipFile module.

from zipfile import ZipFile
import os

#city = 'WashingtonDC'
city = 'SanFrancisco'

for root, dirs, files in os.walk(city, topdown=True): #Run for each city subdirectory
	for filename in files:
		filepath = os.path.join(root, filename)
		print(filepath)
		if filename.endswith('.zip'):
			with ZipFile(filepath, 'r') as zipObj: #Iterate through each .zip file
				for zippedfile in zipObj.namelist(): #Iterate through each file within the .zip file
					if zippedfile.endswith('.csv') and 'MACOSX' not in zippedfile:
						zipObj.extract(zippedfile, root)
                        
                        