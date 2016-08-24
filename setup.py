##
##  Author        : Paul Onions
##  Creation date : 23 August 2016
##
##  Copyright 2016 Silicon Infusion Limited
##
##  Silicon Infusion Limited
##  CP House
##  Otterspool Way
##  Watford WD25 8HP
##  Hertfordshire, UK
##  Tel: +44 (0)1923 650404
##  Fax: +44 (0)1923 650374
##  Web: www.siliconinfusion.com
##
##  Licence: MIT, see LICENCE file for details.
##

##
##  Installation setup script for zaltys-python-utils.
##

from distutils.core import setup

setup(name='zaltys-python-utils',
      version='0.0',
      description='Zaltys python utilities',
      author='Paul Onions',
      author_email='paul_onions@siliconinfusion.com',
      py_modules=['zaltys_ad9361_driver',
                  'zaltys_hdrmd_driver',
                  'zaltys_plsv_utils',
                  'zaltys_smpi_gateway',
                  'zaltys_zwire'])
