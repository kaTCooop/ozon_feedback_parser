import os


modules = ['seleniumbase', 'selenium', 'selenium-stealth', \
           'beautifulsoup4', 'fake-useragent', 'termcolor']

for m in modules:
    os.system('pip3 install ' + m)

