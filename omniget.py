# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:56:43 2014

@author: rjaylward
"""
import sys
import numpy as np
import urllib2
from spacepy import pycdf
import math
import matplotlib.pyplot as plt

def choosedate():

    # import spacepy.toolbox as tb
    
    useinput = raw_input('Use time prompt? ')     
    
    year = input('Year: ')
    month = input('Month: ')
    day = input('Day: ')
    hour = input('Hour: ')    
    minute = input('Minute: ')
    seconds = input('Seconds: ')
        
    
    date = [year,month,day,hour,minute,seconds]

#    timepercent_ion = ((date[3]*3600 + date[4]*60 + date[5])/(24.*60*60))*939
    
#    timevar_ion = int(round(timepercent_ion))
#    print timevar_ion
    
def pastemethod():
    print('Copy and paste times form 1 full day below')
    print('')
    print('Window - Press Control Z and then Enter once you finished')
    print ('Mac - Press Control D')
    text = sys.stdin.read()
    
    prelist = text.split('\n')
    if prelist[-1] == '':
        prelist = prelist[:-1]
    list_of_lists = ['']*len(prelist)
    
    index_count = 0
    for time in prelist:
        list_of_lists[index_count] = time.split(':') 
    
    print list_of_lists
def getomnicdf(date):    
    
#    939
    #http://cdaweb.sci.gsfc.nasa.gov/sp_phys/data/omni/hro_1min/2003/omni_hro_1min_20030101_v01.cdf
    if len(str(date[1])) == 1:
        url = 'http://cdaweb.sci.gsfc.nasa.gov/sp_phys/data/omni/hro_1min/'+ str(date[0]) + '/' + 'omni_hro_1min_' + str(date[0]) + '0' + str(date[1]) + '01_v01.cdf'
    else:
        url = 'http://cdaweb.sci.gsfc.nasa.gov/sp_phys/data/omni/hro_1min/'+ str(date[0]) + '/' + 'omni_hro_1min_' + str(date[0]) + str(date[1]) + '01_v01.cdf'
        
    file_ = 'omni1min' + str(date[0]) + str(date[1]) + '.cdf'
    
    have_cdf = 0
    
    try:
        cdftest = pycdf.CDF(file_)
    except:
        print "Preparing to download..."
    else:
        print "you already have this file"
        have_cdf = 1
        cdftest.close()
    
    if have_cdf == 0:
        f = urllib2.urlopen(url)
        
        f_cdf = open(file_, 'w')
        
        f_cdf.write(f.read())
        
        f_cdf.close() 
    
    with pycdf.CDF(file_) as cdffile1:
        print cdffile1
        
#        array1 = cdffile1['ion_density']
#        print 'this is the ho file'
#        ion_scalar = array1[timevar_ion]
#        print ion_scalar
#        sat_position = array1[hour,0]
#        print ' '
#        print sat_position
#        print ' '
#        #tb.dictree(cdffile)

#    return ion_scalar 

def main():
    
    print 'The default imput method is to use input values with a prompt.'
    print 'Would you like to input days as a list instead? [[year,month,day,hour,min,sec][...]]?)'
    useprompt_ = raw_input('[y/n]: ')
    if useprompt_ == 'n':
        date = choosedate()
   
    getomnicdf(date) 
    
        
if __name__ == "__main__":
	main()