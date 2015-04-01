# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 13:44:56 2014

@author: rjaylward
"""

#def hello():
#    a = raw_input('what is your name? ')
#    b = raw_input('what is your last name? ')
#    return [a,b]
#    
#def printest(a):
#    print a 
#    
#def main():
#    a = hello()
#    printest(a[1])

def main():
    import os
    import urllib2
    from spacepy import pycdf
    import math
    import matplotlib.pyplot as plt
    # import spacepy.toolbox as tb
    
    year = input('Year: ')
    month = input('Month: ')
    day = input('Day: ')
    hour = input('Hour: ')    
    minute = input('Minute: ')
    seconds = input('Seconds: ')
    
    date = [year,month,day,hour,minute,seconds]

    timepercent_ion = ((date[3]*3600 + date[4]*60 + date[5])/(24.*60*60))*939
    
    timevar_ion = int(round(timepercent_ion))
    print timevar_ion
    
#    939
    
    tdpko_url = 'http://cdaweb.sci.gsfc.nasa.gov/sp_phys/data/wind/3dp/3dp_k0/' + str(date[0]) + '/' + 'wi_k0_3dp_' + str(date[0]) + str(date[1]) + str(date[2]) + '_v01.cdf'
    file_tko = 'wi_k0_3dp' + str(year) + str(month) + str(day) + '.cdf'
    
    have_cdftko = 0
    
    try:
        cdftest = pycdf.CDF(file_tko)
    except:
        print "Preparing to download..."
    else:
        print "you already have this file"
        have_cdftko = 1
        cdftest.close()
    
    if have_cdftko == 0:
        f = urllib2.urlopen(tdpko_url)
        
        f_cdf = open(file_tko, 'w')
        
        f_cdf.write(f.read())
        
        f_cdf.close() 
    
    with pycdf.CDF(file_tko) as cdffile1:
#        print cdffile1
        
        array1 = cdffile1['ion_density']
#        print 'this is the ho file'
        ion_scalar = array1[timevar_ion]
        print ion_scalar
#        sat_position = array1[hour,0]
#        print ' '
#        print sat_position
#        print ' '
#        #tb.dictree(cdffile)

    return ion_scalar 

if __name__ == "__main__":
	main()
 