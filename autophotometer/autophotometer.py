#! /usr/bin/env python3
LocalVersion='20230227'

import os
import sys
from sys import stdin
from pkg_resources import get_distribution
isModuleInstalled=1

try:
    import autophotometer.auto_main as auto_main
    
    import autophotometer.coordfix as coordfix
    import autophotometer.starseparator as ss
    import autophotometer.db_extract as db_extract

    
except ImportError:
#ModuleNotFoundError:
    isModuleInstalled=0
    import auto_main

# ==============================================================================
def print_history():
    print('Ver 1.1.0 (2023-Feb-27): Command-line options are introduced to enable different options to be passed to the program.')
    

#######################################################################################
def printHeader(version):
    """ Print the Header """
    print("\n**************************************************************************************")
    print("                         AutoPhotometer: ver.",version)
    print(" ")

def printUsage():
    """ Print the usage info """
    print("Usage:")
    if isModuleInstalled:
        print("AutoPhotometer [options] FitsFile-1 [FitsFile-2]\n")
    else:
        print("python autophotometer.py [options] FitsFile-1 [FitsFile-2]\n")
#    print("autophotometer.py ObsFitsImage1 [ObsFitsImage2]\n")
    print(" ")
    print("AutoPhotometer requires a set of configuration files.")
    print("The program will try to read them from one of the following potential locations:")
    print("   1) the current directory")
    print("   2) ~/.autophotometer in the user’s home directory")
    print("   3) the autophotometer/conf directory from the folder where all the package files are located")
    print(" ")
    print("Options: -abchH")
    print("  -h: Help")
    print("  -H: Summary of changes")
    print("  -a: Astrometric calibration will be performed [default: NO calibration will be performed]")
    print("  -c: Cosmic ray features will be removed       [default: NO CRs will be removed]")
    print("  -b: BackUp files will NOT be created if the above operations will be performed")
    print("                                                [default: BackUp files will be created]")
    print("\n**************************************************************************************\n")

#astrometric calibration

##########################################################################


def cli_main():

    isBackUp    = True
    isCosmic    = False
    isCoordCorr = False
    fits_file1  = None
    fits_file2  = None

    if isModuleInstalled:
        version = get_distribution('autophotometer').version
    else:
        version = LocalVersion+' local\n'

    printHeader(version)
    if len(sys.argv) == 1:
        printUsage()

    for i in range(len(sys.argv)-1):
        CmdLinePar = sys.argv[i+1]
        if (CmdLinePar[0] != '-') and (CmdLinePar[0] != '+'):
            if fits_file1 == None:
                fits_file1 = CmdLinePar
                if not os.path.exists(fits_file1):
                    print("The file", fits_file1, "doesn't exist. Stop executing!")
                    exit()
            elif fits_file2 == None:
                fits_file2 = CmdLinePar
                if not os.path.exists(fits_file2):
                    print("The file", fits_file2, "doesn't exist.")
                    fits_file2  = None

        else:
            if ('h') in CmdLinePar[1:]:
                printUsage()
                exit()
            if ('H') in CmdLinePar[1:]:
                print_history()
                exit()
            if ('a' or 'A') in CmdLinePar[1:]:
                isCoordCorr = True
            if ('c' or 'C') in CmdLinePar[1:]:
                isCosmic = True
            if ('b' or 'B') in CmdLinePar[1:]:
                isBackUp = True


    if fits_file1 == None:
        fits_file1 = input("Enter the filename of the FITS-image or press ENTER: ")
        if len(fits_file1) == 0:
            exit()
        elif not os.path.exists(fits_file1):
            print("The file", fits_file1, "doesn't exist. Stop executing!")
            exit()

    if fits_file2 != None:
        print('\nWARNING! Dual mode (photometric measurements in two Fits-files simultaneously) was NOT tested')
        print('                                                            for a while and my NOT work properly!')
        input("\nPress ENTER:\n")
        auto_main.MainProject_dual(fits_file1, fits_file2, isBackUp, isCosmic, isCoordCorr)
    else:
        auto_main.MainProject(fits_file1, isBackUp, isCosmic, isCoordCorr)

if __name__ == "__main__":
    if not isModuleInstalled:
        sys.stderr.write("\n**************************************************************************************\n")
        sys.stderr.write(" The AutoPhotometer package is not installed!      However, it can be used by running\n")
        sys.stderr.write(" 'python autophotometer.py'  from the folder where all the package files are located.\n")
        # sys.stderr.write(" Also, all the configuration files from ../conf must be copied to the program folder.\n")
    cli_main()
