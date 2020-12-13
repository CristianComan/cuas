#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 10:03:33 2020

@author: Dr Cristian Coman

Version 1.0.0
"""
#print("load cuas_utils.py")


import os, fnmatch
import json

def getFiles(root,pattern,includeSub=False):
    '''
    Returns a list of files with specific name pattern available in a directory "path"
    
    :type root: str
    :type pattern: str - example "2020*.csv"
    :type includeSub: Boolean - include subdirectories
    :rtype: List[str] - list of files including the path
    :rtype: List[str] - list of file names without the path
    
    '''
    # list including the path
    out = []
    
    # list of files without the path
    out1 = []
    
    if includeSub is False:
        # get the list of files in a specific directory
        
        # get the list of files 
        listOfFiles = os.listdir(root)
        
        # check the pattern of th efilename and add to the output lists
        for entry in listOfFiles:
            if fnmatch.fnmatch(entry, pattern):
                out.append(os.path.join(root,entry))
                out1.append(entry)
                
    else:
        # return the list of files including all subfolders
        walk = [root]
        while walk:
            folder = walk.pop(0)+"/"; 
            items = os.listdir(folder) # items = folders + files
            
            for entry in items:
                
                # join the folder and the item: subfolder or file
                entryP = os.path.join(folder,entry) #folder+entry
                
                if os.path.isdir(entryP):
                    walk.append(entryP)
                else:
                    if fnmatch.fnmatch(entry, pattern):
                        out.append(entryP)
                        out1.append(entry)
                

 
    return out, out1

def readJsonByElement(f):
    '''
    Some of the json files are not properly closed. Using jsoan.load will fail. 
    Open the file and read and parse elements by elements. Assumes there is one element by line.
    
    type f: str file name including the path
    rtype List: json data 
    '''
    data = []
    
    with open(f,'r') as filehandle:
        
        for line in filehandle:
            try:
                data.append(json.loads(line))
            except:
                print('Incorrect json element in file {}'.format(f))
                                            
    filehandle.close()
       
    return data


def loadData(f):
    '''
    Load data from a json file. In case the json file is not closed properly, 
    use readJsonByElement and save the file with the same name.
    
    type f: str file name including the path
    rtype List: json data
    '''
    with  open(jsonFile,'r') as filehandle:
        
        try:
            data = json.load(filehandle)
            filehandle.close()
            
        except:
            print('Could not load file {}. Read element by element.'.format(f))
            
            filehandle.close()
            
            data = readJsonByElement(f)
            
            nf = f[:-5] + '_corrected.json'
            
            print('Save the corrected file with the name {}'.format(nf))
            
            with open(nf,'w') as newfilehandle:
                json.dumps(data,newfilehandle)
                
                newfilehandle.close()
            
            
    return data
            
            
                
        
    

def correctJson(fnameList):
    '''
    Some json files are missing a "} closing characters
    
    '''
    
    for item in fnameList:
        with open(item,'a') as file:
            
            file.write("\"}")
            file.close()
            
            '''
            ADD verification if the file has alraedy been processed
            
            # seek to the end of the file
            
            print(file.tell())
            
            file.seek(-1,2)
            
            # check if the last closing characters are there
            
            
            if file.read(1) != "}":
            # add closing tags
                file.seek(0,2)      
                file.write("\"}")
    
            file.close()
            '''

if __name__ == "__main__":
    
    root = "./Red Team/SensorData"
    pattern = "*.json"
    
    lofp, lof  = getFiles(root,pattern,True)
    
    
    jsonFile = lofp[0]
    
    print(jsonFile)
    
    data = readJsonByElement(jsonFile)
    
    filehandle = open(jsonFile,'r')
    data = json.load(filehandle)
    print(data)

    # read line by line
    '''
    f = open("./Red Team/SensorData/2020/10/01/11_00_00_sbs-2.json",'r')

    f.readline()
    Out[90]: '{"time_stamp":{"seconds":"1601550000","nanoseconds":0},"raw_data":"FQAu+6NRhjRCACBNWAAAkZSkABtTuEQCjQAHCAV4AAAHWnvcFXHzyQggAiLcGw=="}\n'

    j = json.loads(f.readline())

    j
    Out[92]: 
    {'time_stamp': {'seconds': '1601550000', 'nanoseconds': 10000000},
         'raw_data': 'FQAu+6NRhjRCACBNWAAAk8+AABO0nIlkpwAHCAVQAAAIqtEFVBFywxggBQa5Eg=='}
    '''
    
    # decode base64
    
    '''
    raw64 = "ICAgPEF6aW11dGg+MjEzLjE3NjA1NTkxPC9BemltdXRoPgogICAgICAgICAgICAgICAgPEVsZXZhdGlvbj4tOC45NjE3OTg2NzwvRWxldmF0aW9uPgogICAgICAgICAgICAgICAgPFNwZWVkPjkuNDAwMTk2MDg8L1NwZWVkPgogICAgICAgICAgICA8L1ZlbG9jaXR5PgogICAgICAgICAgICA8Q2xhc3NpZmljYXRpb24+T1RIRVI8L0NsYXNzaWZpY2F0aW9uPgogICAgICAgICAgICA8UmVmbGVjdGlvbj4tMjguMzI2MzM5NzI8L1JlZmxlY3Rpb24+CiAgICAgICAgICAgIDxTY29yZT4wLjg4MDI3NzUxPC9TY29yZT4KICAgICAgICAgICAgPEFsYXJtPmZhbHNlPC9BbGFybT4KICAgICAgICA8L1RyYWNrPgogICAgICAgIDxUcmFjayBpZD0iOTI1NCI+CiAgICAgICAgICAgIDxUaW1lc3RhbXA+MjAyMC0xMC0wMVQwODoxNjoxOS4xNTlaPC9UaW1lc3RhbXA+CiAgICAgICAgICAgIDxQb3NpdGlvbj4KICAgICAgICAgICAgICAgIDxMYXRpdHVkZT41MS41MjQwMjc1OTwvTGF0aXR1ZGU+CiAgICAgICAgICAgICAgICA8TG9uZ2l0dWRlPjUuODY2OTI0NzU8L0xvbmdpdHVkZT4KICAgICAgICAgICAgICAgIDxBbHRpdHVkZT40OS45OTUxMTA5NTwvQWx0aXR1ZGU+CiAgICAgICAgICAgIDwvUG9zaXRpb24+CiAgICAgICAgICAgIDxWZWxvY2l0eT4KICAgICAgICAgICAgICAgIDxBemltdXRoPjI1Ny43MDIzMDEwMzwvQXppbXV0aD4KICAgICAgICAgICAgICAgIDxFbGV2YXRpb24+LTMuNDIxMTAxMzM8L0VsZXZhdGlvbj4KICAgICAgICAgICAgICAgIDxTcGVlZD4xOC41ODg2MjMwNTwvU3BlZWQ+CiAgICAgICAgICAgIDwvVmVsb2NpdHk+CiAgICAgICAgICAgIDxDbGFzc2lmaWNhdGlvbj5WRUhJQ0xFPC9DbGFzc2lmaWNhdGlvbj4KICAgICAgICAgICAgPFJlZmxlY3Rpb24+LTEwLjU3NTgxNzExPC9SZWZsZWN0aW9uPgogICAgICAgICAgICA8U2NvcmU+MC44OTYxNTk1MzwvU2NvcmU+CiAgICAgICAgICAgIDxBbGFybT5mYWxzZTwvQWxhcm0+CiAgICAgICAgPC9UcmFjaz4KICAgICAgICA8VHJhY2sgaWQ9IjkyNjciPgogICAgICAgICAgICA8VGltZXN0YW1wPjIwMjAtMTAtMDFUMDg6MTY6MDkuODE2WjwvVGltZXN0YW1wPgogICAgICAgICAgICA8UG9zaXRpb24+CiAgICAgICAgICAgICAgICA8TGF0aXR1ZGU+NTEuNTIwMTE0MTI8L0xhdGl0dWRlPgogICAgICAgICAgICAgICAgPExvbmdpdHVkZT41Ljg2NTAwNTAyPC9Mb25naXR1ZGU+CiAgICAgICAgICAgICAgICA8QWx0aXR1ZGU+OTIuMzMzOTI2OTI8L0FsdGl0dWRlPgogICAgICAgICAgICA8L1Bvc2l0aW9uPgogICAgICAgICAgICA8VmVsb2NpdHk+CiAgICAgICAgICAgICAgICA8QXppbXV0aD4xOTkuNzE3ODk1NTE8L0F6aW11dGg+CiAgICAgICAgICAgICAgICA8RWxldmF0aW9uPjQ4LjAwODA3OTUzPC9FbGV2YXRpb24+CiAgICAgICAgICAgICAgICA8U3BlZWQ+MTEuODE0NDY0NTc8L1NwZWVkPgo="
    
    raw64a = raw64.encode('ascii')

    raw64b = base64.b64decode(raw64a)

    raw64c = raw64b.decode('ascii')
    
    '''
    
    
    # correctJson(lofp)
    
    
    '''
    # for test purposes create a test.json with the following string
    # {'time_stamp': {'seconds': '1601530621', 'nanoseconds': 430000000}, 'raw_data': 'FQAu+6NRhjRCACAnfoAAkYOqABHz1jxl1QAHCAXvAAAHU867EMIzQOggAgGMAA=='}
    
    jsonFile = "./Red Team/SensorData/2020/10/01/test.json"
    
    print(jsonFile)
    
    correctJson(['./Red Team/SensorData/2020/10/01/test.json'])
    
    filehandle = open(jsonFile,'r')
    try:
        data = json.load(filehandle)
        print(data)
    except:
        print('could not parse the json')
    
    '''