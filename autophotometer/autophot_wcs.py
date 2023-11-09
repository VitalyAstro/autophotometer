"""implant wcs information into image header
michael.mommert@nau.edu, Mar 21, 2017
https://github.com/mommermi/2017Spring_Astroinformatics

The script implants all the necessary for SCAMP information 
into all FITS files in the same directory.

The original script was modified to be able to work with
ESO NTT/EFOSC and NTT/SOFI images.
vitaly@neustroev.net, Aug 22, 2021

Nov 9, 2023: Optimized for SOFI
"""

import os
from astropy.io import fits

for filename in os.listdir('.'):
    if not '.fits' in filename:
        continue

    hdu = fits.open(filename, mode='update')
    header = hdu[0].header

    if header['TELESCOP'] == 'ESO-NTT' and (header['INSTRUME'] == 'SOFI' or 'EFOSC'):
        print('File',filename,'was taken with',header['TELESCOP'],'/',header['INSTRUME'],'and its header will be modified to be used with SCAMP.')
    
        header['CRTYPE1'] = 'RA---TAN'
        header['CRTYPE2'] = 'DEC--TAN'  
        header['CTYPE1']  = 'RA---TAN'
        header['CTYPE2']  = 'DEC--TAN'
        header.set('RADECSYS','FK5')

        #if header['INSTRUME'] == 'SOFI' or 'EFOSC':
        if header['INSTRUME'] == 'SOFI':
            print('Filter',header['HIERARCH ESO INS FILT1 NAME'])
            header.set('WCSDIM',2)  # Not sure if this needed.
            header.set('FILTER1',header['HIERARCH ESO INS FILT1 NAME'],'Filter Name.')
            header.set('CRPIX1',559.0,'Ref. pixel of center of rotation.')
            header.set('CRPIX2',546.5,'Ref. pixel of center of rotation.')
            header.set('CRVAL1',header['RA'],'Value of ref pixel.')
            header.set('CRVAL2',header['DEC'],'Value of ref pixel.')
            header.set('CD1_1',-3.528176553074E-08,'Translation matrix element.')
            header.set('CD2_2',3.53111279900792E-08,'Translation matrix element.')
            header['HISTORY'] ='Keywords FILTER1, CRPIX1, CRPIX2, CRVAL1, CRVAL2, CD1_1, CD2_2  were set'
        header.set('CD1_2',-8.0018968846984E-05,'0 if no field rotation.',after='CD1_1')
        header.set('CD2_1',-7.995243022721E-05,'0 if no field rotation.',before='CD2_2')    
        header['HISTORY'] ='Keywords CRTYPE1, CRTYPE2, CD1_2, CD2_1 were set'
        
        if header['INSTRUME'] == 'EFOSC':
            print('Filter',header['FILTER1'])
            header.set('GAIN',header['HIERARCH ESO DET OUT1 GAIN'],'Conversion from electrons to ADU (e-/ADU).')
            header.set('RON',header['HIERARCH ESO DET OUT1 RON'],'Readout noise per output (e-).')
            header['HISTORY'] ='Keywords GAIN and RON were set'
        else:
            header.set('GAIN',5.4,'Conversion from electrons to ADU (e-/ADU).')
            header.set('RON',12.0,'Readout noise per output (e-).')
            header.set('RONADU',2.1,'Readout noise per output (ADU).')
            header.set('AIRMASS',header['HIERARCH ESO TEL AIRM START'],'Airmass at start')
            header['HISTORY'] ='Keywords GAIN, RON, RONADU, and AIRMASS were set'
        hdu.flush()
    else:
        print('File',filename,'was taken with a not supported telescope or instrument. Skipped.')
