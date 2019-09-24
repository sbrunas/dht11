import ftplib
ftp = ftplib.FTP('201.215.167.63', 'pi', '_4oYiEmqVUFl')
ftp.cwd('/')
filematch = 'ftptest.txt'
target_dir = '/home/pi/nextcloud/data/__groupfolders/1/log'
import os

for filename in ftp.nlst(filematch):
    target_file_name = os.path.join(target_dir, os.path.basename(filename))
    with open(target_file_name ,'wb') as fhandle:
        ftp.retrbinary('RETR %s' % filename, fhandle.write)