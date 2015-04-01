# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 17:20:11 2014

@author: rjaylward
"""

def main():
    import os
    import urllib2
    from spacepy import pycdf
    import math
    # import spacepy.toolbox as tb
    
    year = input('Year: ')
    month = input('Month: ')
    day = input('Day: ')
    hour = input('Hour: ')    
    minute = input('Minute: ')
    seconds = input('Seconds: ')
    

    timepercent = ((hour*3600 + minute*60 + seconds)/(24.*60*60))*884
    
    timevar = int(math.floor(timepercent))
    print timevar
    
    mfiho_url = 'http://cdaweb.sci.gsfc.nasa.gov/sp_phys/data/wind/mfi/mfi_h0/' + str(year) + '/' + 'wi_h0_mfi_' + str(year) + str(month) + str(day) + '_v05.cdf'
    
    file_ho = 'wi_h0_mfi' + str(year) + str(month) + str(day) + '.cdf'
    
    have_cdfho = 0
    
    try:
        cdftest = pycdf.CDF(file_ho)
    except:
        print "Preparing to download..."
    else:
        print "you already have this file"
        have_cdfho = 1
        cdftest.close()
    
    if have_cdfho == 0:
        f = urllib2.urlopen(mfiho_url)
        
        f_cdf = open(file_ho, 'w')
        
        f_cdf.write(f.read())
        
        f_cdf.close() 
    
#    with pycdf.CDF(file_ho) as cdffile1:
#        print cdffile1
#        array1 = cdffile1['P1GSM']
#        print 'this is the ho file'
#        print array1[:,0]
#        sat_position = array1[hour,0]
#        print ' '
#        print sat_position
#        print ' '
#        #tb.dictree(cdffile)
#        
#        corrected_position = sat_position + ((array1[hour + 1,0] - array1[hour,0]) / 60.) * minute
#        print corrected_position 

    with pycdf.CDF(file_ho) as cdffile1:
        print cdffile1
        array1 = cdffile1['BGSM']
        print 'this is the ho file'
        print array1[:,0]
        bx = array1[minute,0]
        by = array1[minute,1]
        bz = array1[minute,2]
        print ' '
        print bx
        print by
        print bz
        print ' '
        #tb.dictree(cdffile)
        
        mag_vector = [bx,by,bz]
        
        return mag_vector 

if __name__ == "__main__":
	main()