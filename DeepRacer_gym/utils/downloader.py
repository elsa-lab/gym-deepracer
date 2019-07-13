import os
import sys
import time 
import logging

import errno
import subprocess

import zipfile

def make_dirs(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

class GoogleDriveDownloader:
    @staticmethod
    def check_or_download(executable_path, download_id, filename, large_file=True, make_executable=True):
        
        if os.path.isfile(executable_path):
            return True

        dirname = os.path.dirname(executable_path)
        make_dirs(dirname)

        name = os.path.basename(filename)

        try:
            if large_file:
                subprocess.run("wget --save-cookies cookies.txt 'https://docs.google.com/uc?export=download&id='{} -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\\1/p' > confirm.txt".format(download_id), shell=True)
                subprocess.run("wget --load-cookies cookies.txt -O {} 'https://docs.google.com/uc?export=download&id='{}'&confirm='$(<confirm.txt)".format(name, download_id), shell=True)

                subprocess.run(['rm', 'cookies.txt'])
                subprocess.run(['rm', 'confirm.txt'])

            else:
                subprocess.run("wget -O {} 'https://docs.google.com/uc?export=download&id='{}".format(name, download_id), shell=True)
        except:
            raise

        with zipfile.ZipFile(filename, 'r') as zip_file:
            zip_file.extractall(path=dirname)


        if make_executable:
            subprocess.run("chmod +x {}".format(executable_path), shell=True)
        
        return True


