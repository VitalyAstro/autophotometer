#! /usr/bin/env python3
from astropy.io import fits
import subprocess
import ccdproc
import os # Vitaly 20211108
from pathlib import Path # Vitaly 20230227
path_root = Path(__file__).parents[2]
path_src_conf = str(path_root) +'/autophotometer/conf/'

def runscamp2mass():
#Vitaly 20230227
    ph1cat_file='phase1.cat'
    if not os.path.exists(ph1cat_file):
        ph1cat_file = os.path.expanduser('~/.autophotometer/phase1.cat')
    if not os.path.exists(ph1cat_file):
        ph1cat_file = path_src_conf+'phase1.cat'
    if not os.path.exists(ph1cat_file):
        print('\nWARNING! The config file "phase1.cat" is NOT found!!!')
        input("\nPress ENTER: ")

    scampconf_file='scamp.conf'
    if not os.path.exists(scampconf_file):
        scampconf_file = os.path.expanduser('~/.autophotometer/scamp.conf')
    if not os.path.exists(scampconf_file):
        scampconf_file = path_src_conf + 'scamp.conf'
    if not os.path.exists(scampconf_file):
        print('\nWARNING! The config file "scamp.conf" is NOT found!!!')
        input("\nPress ENTER: ")
#Vitaly 20211108
    subprocess.call(['scamp', "-c", scampconf_file, ph1cat_file, '-ASTREF_CATALOG', '2MASS'])


def runscamp():
#Vitaly 20230227
    ph1cat_file='phase1.cat'
    if not os.path.exists(ph1cat_file):
        ph1cat_file = os.path.expanduser('~/.autophotometer/phase1.cat')
    if not os.path.exists(ph1cat_file):
        ph1cat_file = path_src_conf+'phase1.cat'
    if not os.path.exists(ph1cat_file):
        print('\nWARNING! The config file "phase1.cat" is NOT found!!!')
        input("\nPress ENTER: ")

    scampconf_file='scamp.conf'
    if not os.path.exists(scampconf_file):
        scampconf_file = os.path.expanduser('~/.autophotometer/scamp.conf')
    if not os.path.exists(scampconf_file):
        scampconf_file = path_src_conf + 'scamp.conf'
    if not os.path.exists(scampconf_file):
        print('\nWARNING! The config file "scamp.conf" is NOT found!!!')
        input("\nPress ENTER: ")

#Vitaly 20230227
    subprocess.call(['scamp', "-c", scampconf_file, ph1cat_file])

def runsex(fits_file):
    # Vitaly 20230227
    sexdef_file='default.sex'
    if not os.path.exists(sexdef_file):
        sexdef_file=os.path.expanduser('~/.autophotometer/default.sex')
    if not os.path.exists(sexdef_file):
        sexdef_file = path_src_conf + 'default.sex'
    if not os.path.exists(sexdef_file):
        print('\nWARNING! The config file "default.sex" is NOT found!!!')
        input("\nPress ENTER: ")

    run1_file = 'run1.param'
    if not os.path.exists(run1_file):
        run1_file=os.path.expanduser('~/.autophotometer/run1.param')
    if not os.path.exists(run1_file):
        run1_file = path_src_conf + 'run1.param'
    if not os.path.exists(run1_file):
        print('\nWARNING! The config file "run1.param" is NOT found!!!')
        input("\nPress ENTER: ")



    subprocess.call(['sex', "-c", sexdef_file, fits_file, "-PARAMETERS_NAME", run1_file])
# Vitaly 20211108


def read_header(filename): #function that reads .head files created by SCAMP
    headerlines = []
    with open(filename) as f:
        for line in f.readlines()[3:-1]:
            line = line.replace('/', '=').strip()	#removing all extra bits from the lines
            line = line.split('=')
            value = line[1].replace("'",'').strip()
            try:	#convert the values into floats if possible
                line[1] = float(value)
            except ValueError:
                line[1] = value
            headerlines.append(line)	#put all elements in a single list
    return headerlines

def fits_backup(fits_file):
    fits_inf = fits.open(fits_file, 'update', save_backup=True)
    #fits_inf.info()
    fits_inf.close()


def addheads(fits_head, fits_file):
    heads = read_header(fits_head)
    for head in heads:
        try:
            fits.delval(fits_file, head[0])
        except KeyError:
            continue
        fits.setval(fits_file, head[0], value=head[1])

def cosmics(fits_file):
    hdu = fits.open(fits_file, mode = 'update')
    image = hdu[0].data
    header = hdu[0].header
    try:
        gain = header['GAIN']
    except:
        try:
            gain = header['GAIN1'] #some images seem to have multiple gain keywords.
        except:
            gain = 1 #if no gain found, set it to 1 and hope for the best.
            print('No gain keyword is found. GAIN = 1 will be used for cosmic features removal.')
            input("\nPress ENTER: ")
    hdu[0].data = ccdproc.cosmicray_lacosmic(image, gain = gain)[0]
    hdu.close()

def coordcorr(fits_file, filt, isBackUp, isCosmic, isCoordCorr):
    fits_head = 'phase1.head'

    if (isCosmic or isCoordCorr) and isBackUp:
        print('WARNING! A backUp file will be created before')
    else:
        print('No corrections (cosmic ray features removal, astrometric calibration) will be done.')
    if (isCosmic and isCoordCorr):
        print('------>  cosmic ray features removal and')
    if isCosmic:
        print('------>  cosmic ray features removal.')
    if isCoordCorr:
        print('------>  astrometric calibration.')
        
    input("\nPress ENTER: ")
    
    if (isCosmic or isCoordCorr) and isBackUp:
        fits_backup(fits_file)
        if isCosmic:
            cosmics(fits_file)
        if isCoordCorr:
            runsex(fits_file)
        if filt in ['J', 'H', 'K']:
            runscamp2mass()
        else:
            runscamp()
            addheads(fits_head, fits_file)
            print('----Done!----')



    #print('Do you want to make changes to', fits_file,'before continuing?\n[y]es, [n]o, [q]uit.')
    #while True:
        #query = str(input('y/n/q: ')).lower()
        #if query == 'y':
            #print('Do you want to make a backup of the file?')
            #bak_query = str(input('y/n: ')).lower()

            #print('Do you want to remove cosmic rays?')
            #cosmic_query = str(input('y/n: ')).lower()

            #print('Do you want to do the coordinate correction?')
            #corr_query = str(input('y/n: ')).lower()

            #if bak_query == 'y':
                #fits_backup(fits_file)

            #if cosmic_query == 'y':
                #cosmics(fits_file)

            #if corr_query == 'y':
                #runsex(fits_file)
                #if filt in ['J', 'H', 'K']:
                    #runscamp2mass()
                #else:
                    #runscamp()
                #addheads(fits_head, fits_file)
                #print('----Done!----')
            #break
        #elif query == 'n':
            #break
        #elif query == 'q':
            #exit()

        #else:
            #print('Unknown input.')
