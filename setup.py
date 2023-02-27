from setuptools import setup, find_packages
import os

setup(
    name='autophotometer',
    version='1.1.0',
    url='https://github.com/VitalyAstro/autophotometer.git',
    author='Vitaly Neustroev, Aleksi Mattila',
    author_email='vitaly.neustroev@gmail.com',
    description='A semi-automatic pipeline for photometric measurements',
    python_requires='>=3.7',
    install_requires=[
    install_requires=[
        'numpy >= 1.20.2',      #works with 1.21.4
        'astropy >= 4.2.1',
        'ccdproc >= 2.2.0',
        'photutils >= 1.2.0',   #works with 1.3.0
        'plotille >= 3.8.0',    #works with 4.0.2
        'requests >= 2.25.1',   #works with 2.28.1
        'scipy >= 1.4.1',
        'matplotlib >= 3.4.1'], #works with 3.5.0   
    packages=['autophotometer'],
#    package_dir={'autophoto': 'src/mypkg'},
#    package_data={'mypkg': ['data/*.dat']},

    package_data={'autophotometer': ['conf/*']},
    data_files=[(os.path.expanduser('~/.autophotometer'), ['conf/conf_autophot.ini','conf/default.nnw','conf/default.psf',
                                   'conf/default.sex','conf/ph2conf.sex','conf/run1.param','conf/run2.param','conf/scamp.conf'])],
    include_package_data=True,
    entry_points = {'console_scripts': ['AutoPhotometer=autophotometer.autophotometer:cli_main']},
)
