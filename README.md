# AutoPhotometer

AutoPhotometer is a semi-automatic Python based pipeline for photometric measurements.
It was developed as part of Master's Thesis of [Aleksi Mattila](https://github.com/almattil/autophotometer) under my supervision, but now I forked the program and continue its development on my own. 

AutoPhotometer uses Source Extractor and SCAMP to find the detections from the user's FITS images, and finds matches for them from an online database. 
AutoPhotometer's objective is to provide a quick and easy way to study variable and transient stars, but can be used for other types of objects as well.

### Prerequisites
AutoPhotometer requires [SExtractor](https://github.com/astromatic/sextractor) version 2.25.0 or newer,
[SCAMP](https://github.com/astromatic/scamp) version 2.10.0 or newer, and their software requirements. 
Additionally it uses the following python packages: 
  - Astropy
  - Numpy
  - Matplotlib
  - Scipy
  - photutils
  - CCDProc
  - Plotille
  - Requests

AutoPhotometer was developed using Python 3.8 (also known to work in Python 3.7.5).

### How to use AutoPhotometer without installing it on a computer?

If all the necessary python packages are already installed on the computer, then AutoPhotometer can be used without proper installation.
Download the source archive from GitHub and unpack it in a directory of your choice.
Run the program and read Help:

    python path-to-dir/autophotometer/autophotometer/autophotometer.py

### Installing - Using pip

You can get the source code from github by typing into your terminal:

    git clone https://github.com/VitalyAstro/autophotometer

To update to the latest version, change into the directory where the code resides on your computer and type into your terminal:

    git pull

Install the program using command

    pip --user install .
    
in the directory of the downloaded files. 
The use of flag --user is recommended, so the program is installed for only the current user. 
It should be noted that when installing in a virtual environment, --user is not necessary.

## Usage

AutoPhotometer currently has two modes: single image and dual image operations. In single mode the program processes only one image, and in dual mode it runs two images of the field in different filter bands. Dual image mode compares the images to each other and outputs values for the detections in both images.

The dual mode is more constricted, as it only uses detections present in both images, which can cause some issues. The dual image functionality may be removed in future, as the single image mode gives more reliable results.

Running the program is done using the terminal. It can be called from any directory using the command (if the program installed using pip):

    AutoPhotometer [options] [images]

The argument "images" can contain up to two FITS files, depending on which mode you want to use. The program finds the used filter bands from the fits headers, and will give an error if a filter is unsupported. The fits header must contain keywords that describe the coordinate system, coordinate system reference pixels, and other keywords for SCAMP to be able to process them.

**Note that before measurements, the FITS-file must be astrometric calibrated and, preferably, cleaned for cosmic ray features.**
AutoPhotometer can remove cosmic features and perform the coordinate correction (see Help for the flags). Because these operations modify the fits files, the program can create a backup of the original file if necessary.

Then the program shows two histograms. The first histogram shows all the FWHM values of the detections in arcseconds. In the second histogram only the detections within a threshold are kept. This is done to exclude detections with too big or small FWHM, which might be galaxies, clusters, cosmic rays, or other non-star objects. The detections that are left are most likely stars.

Then the program shows a figure of the colour term calculations. In the figure the X-axis shows the difference in magnitudes between two adjacent filters and the Y-axis shows the uncorrected instrumental magnitudes. A linear fit to the data is used to find the extinction coefficient and zero point magnitude. The figure can be used to evaluate whether the fit is good or not.

Finally the program draws the fits image, with markers depicting the different detection types and if the detections are present in the database. Note that in the figure, some detections are left unmarked. The detection threshold can be adjusted in the conf\_autophotometer.ini file. 

When a marker is clicked, the program outputs the coordinates of the detected source in degrees, magnitudes, database magnitudes, and errors in the terminal. The program also saves the information of the selected detections and writes it into a file called "Selected\_Mags\_[image name].dat," which is generated in the directory where the program is executed. 

## Example

We provide two FITS-files to play with the program. They are located in the directory example.

The file V455And_V_corrected.fits has already cosmic features removed and is coordinate corrected, while V455And_V_original.fits is the original file for which the above operations **should be applied**:

    AutoPhotometer -ac V455And_V_original.fits

For the corrected file no flags are needed:

    AutoPhotometer V455And_V_corrected.fits
