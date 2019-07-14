import os
import sys
import time 
import logging

import errno
import subprocess

import zipfile

from DeepRacer_gym.utils.universal import UNIVERSAL_LOCK

LOG = logging.getLogger()


def make_dirs(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def run_command(command, shell=False):
    LOG.info("execute command: {}".format(command))
    return subprocess.run(command, shell=shell)


class GoogleDriveDownloader:
    @staticmethod
    def check_or_download(executable_path, download_id, filename, large_file=True, make_executable=True):
        
        with UNIVERSAL_LOCK.get_lock():

            if os.path.isfile(executable_path):
                return True
            else:
                LOG.warning("Executable file does not exist: {}".format(executable_path))
                LOG.info("Downloading.....")

            dirname = os.path.dirname(executable_path)
            make_dirs(dirname)

            name = os.path.basename(filename)

            try:
                if large_file:
                    run_command("wget --save-cookies cookies.txt 'https://docs.google.com/uc?export=download&id='{} -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\\1/p' > confirm.txt".format(download_id), shell=True)
                    run_command("wget --load-cookies cookies.txt -O {} 'https://docs.google.com/uc?export=download&id='{}'&confirm='$(<confirm.txt)".format(filename, download_id), shell=True)

                    run_command(['rm', 'cookies.txt'])
                    run_command(['rm', 'confirm.txt'])

                else:
                    run_command("wget -O {} 'https://docs.google.com/uc?export=download&id='{}".format(filename, download_id), shell=True)
            except:
                raise

            with zipfile.ZipFile(filename, 'r') as zip_file:
                zip_file.extractall(path=dirname)


            if make_executable:
                run_command("chmod +x {}".format(executable_path), shell=True)
        
        return True


