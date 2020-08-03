#Download all the bike data .zip or .csv data files from the specified cities

import requests
from bs4 import BeautifulSoup
import wget

#Cities and data page URLs 
bikeSites = {
    'Philadelphia': 'https://s3.amazonaws.com/divvy-data', 
    'NewYork': 'https://s3.amazonaws.com/tripdata',
    'Boston': 'https://s3.amazonaws.com/hubway-data',
    'WashingtonDC': 'https://s3.amazonaws.com/capitalbikeshare-data',
    'SanFrancisco': 'https://s3.amazonaws.com/baywheels-data'
    }

localpath = ''
logfile = open('pythonlog.txt', 'w+')

#Iterate through city/URL dictionary
for city, url in bikeSites.items():

    print(city)
    logfile.write(city + '\r\n')
    try:
        document = requests.get(url) #Get data page HTML
    except:
        logtext = 'ERROR: Document request failed for city: ' + city + '\r\n'
        print(logtext)
        logfile.write(logtext)
        continue
    
    try:
        soup = BeautifulSoup(document.content,"lxml-xml") #Create Beautiful Soup XML object
    except:
        logtext = 'ERROR: BeautifulSoup request failed for city: ' + city + '\r\n'
        print(logtext)
        logfile.write(logtext)
        continue
    
    #All the data pages have a similar format, 
    #with the file name in the Key element
    
    #<Contents>
    #    <Key>201801-fordgobike-tripdata.csv.zip</Key>
    #    <LastModified>2019-06-07T20:52:29.000Z</LastModified>
    #    <ETag>"52b0d1014a2a9f831b77275299e00282"</ETag>
    #    <Size>3329766</Size>
    #    <StorageClass>STANDARD</StorageClass>
    #</Contents>

    #Parse out all the Key element values
    for tag in soup.find_all('Key'):
        filepath = tag.contents[0]
        if filepath.endswith('zip') or filepath.endswith('csv'):
            if city == 'Philadelphia':
                filename = filepath.replace('tripdata/', '')
            else:
                filename = filepath
                
            #print('filepath: ' + filepath)
            #print('filename: ' + filename)
            downloadurl = url + '/' + filepath
            print('downloadurl: ' + downloadurl)

            try:
                print('Downloading ' + filename + '. Please wait...')
                logfile.write(filename + '\r\n')
                
                #Use wget module to download the file
                wget.download(downloadurl, city + '/' + filename)
            except:
                logtext = 'ERROR: File download failed for city: ' + city + ' file: ' + filename + '\r\n'
                print(logtext)
                logfile.write(logtext)
                continue                
    print()
     
logfile.close()
