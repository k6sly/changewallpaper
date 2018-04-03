''' This program downloads a new image form the Astronomy Picture of the Day website and installs
    the new image in a temp folder for Dual Monitory Tools to pickup and add to wallpaper backgrounds
'''

import datetime
import os
import subprocess
from configparser import ConfigParser
# from os import system

import certifi
import urllib3
from bs4 import BeautifulSoup


def getini(ini):
    config = ConfigParser()
    wd = os.getcwd()
    config.read(wd + "/wallpaper.ini")
    getline = config.get('settings', ini)

    return getline


def getdatetime():

    d = datetime.date.today()

    day = str('{:02d}'.format(d.day))
    month = '{:02d}'.format(d.month)
    year = d.year-2000

    seq = (str(year), str(month), str(day))
    s = ""
    return s.join(seq)


def getimage():
    try:
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        base_url = getini('base_url')

        if getini('date'):
            url = base_url + '/ap' + getini('date') + '.html'
        else:
            url = base_url + '/ap' + getdatetime() + '.html'

        default_dir = getini('default_dir')

        response = http.request('GET', url)
        soup = BeautifulSoup(response.data, "html.parser")
        imgs = soup.find_all("img", {"alt":True, "src":True})
        img_url_raw = imgs[0]
        img_url = img_url_raw["src"]
        img_url_full = base_url + '/' + img_url
        filename = os.path.join(default_dir + getini('tempfolder'), img_url_full.split("/")[-1])
        img_data = http.request('GET', img_url_full)
        f = open(filename, "wb")
        f.write(img_data.data)
        f.close()
        shellprocesses()
    except IndexError:
        print('No Images Available')


def shellprocesses():
        #dualmonitortools(0)
        screens = int(getini('numScreens'))
        default_dir = getini('default_dir')
        t = 'Del ' + default_dir + str(screens) + '\*.* /Q'
        subprocess.Popen(t, shell=True)
        screens -= 1
        while screens > 0:
            t = 'Move ' + default_dir + str(screens) + '\\*.* ' + default_dir + str(screens + 1) + '\\'
            subprocess.Popen(t, shell=True)
            screens -= 1
        t = 'Move ' + default_dir + getini('tempfolder') + '\\*.jpg ' + default_dir + '1\\'
        subprocess.Popen(t, shell=True)
        #dualmonitortools(1)


'''
def dualmonitortools(status):
    exe = os.path.normcase(getini('dualMonitor'))
    try:
        if status == 0:
            flag = ' ' + getini('dualMonitorFlag')
            #process = subprocess.Popen(exe + flag, shell=True)
            #subprocess.Popen(exe)
        else:
            process = subprocess.Popen(exe, shell=True)
            #subprocess.Popen(exe)
    except FileNotFoundError:
        print('Cannot find Dual Monitor Tools at the supplied path ' + tools)
    finally:
        pass
'''

if __name__ == '__main__':
    getimage()
