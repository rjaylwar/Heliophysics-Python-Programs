# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/Users/rjaylward/.spyder2/.temp.py
"""
def getcdfmfiho():
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
    
    with pycdf.CDF(file_ho) as cdffile1:
        #print cdffile
        array1 = cdffile1['P1GSM']
        print 'this is the ho file'
        print array1[:,0]
        sat_position = array1[hour,0]
        print ' '
        print sat_position
        print ' '
        #tb.dictree(cdffile)
#    
#        
#    print sat_position
    file_ko = 'wi_k0_swe' + str(year) + str(month) + str(day) + '.cdf'
    
    have_cdf = 0
    
    try:
        cdftest = pycdf.CDF(file_ko)
    except:
        print "Preparing to download..."
    else:
        print "you already have this file"
        have_cdf = 1
        cdftest.close()
        
        
    sweko_url = 'http://cdaweb.sci.gsfc.nasa.gov/sp_phys/data/wind/swe/swe_k0/' + str(year) + '/' + 'wi_k0_swe_' + str(year) + str(month) + str(day) + '_v01.cdf'
    # note, sometimes it is not v01, could be v02, or v05
    if have_cdf == 0:
        f = urllib2.urlopen(sweko_url)
    
        f_cdf = open(file_ko, 'w')
        
        f_cdf.write(f.read())
        
        f_cdf.close() 
        
    dontquit = 1
    endearly = 1
    timevar_copy = timevar
    
    with pycdf.CDF(file_ko) as cdffile2:
        # print cdffile2
        array2 = cdffile2['V_GSM']
        swvelocity = array2[timevar,0]
        if swvelocity > -200 or swvelocity < -900 and swvelocity > -1000:
            print "Solar wind speed is: " + str(swvelocity) 
            advance = raw_input('Try the Solar Wind speed 1.5 min later? (y/n) ')
            
            if advance == 'Y' or advance == 'y' or advance == 'Yes' or advance == 'YES' or advance == 'yes':
                timevar += 3 
                swvelocity = array2[timevar, 0]
                while swvelocity < -900 and endearly:
                    timevar += 3
                    swvelocity = array2[timevar, 0]
                    if timevar - timevar_copy > 30:
                        endearly = 0
                if endearly == 0:
                    print ('Solar wind velocity data unavilible.')

            elif advance == 'N' or advance == 'n' or advance == 'No' or advance == 'NO' or advance == 'no':
                print "Warning, check the plot to verify this data"
            else:
                advance = raw_input('Input not recognized. Try Solar Wind speed 3 min later? (y/n) ')
                
        elif swvelocity < -1000:
            ### could also add a loop here to check...
            print "Solar wind velocity data unavalible for this time period"
            advance = raw_input('Use Solar Wind speed 3 min later? (y/n) ')
            
            if advance == 'Y' or advance == 'y' or advance == 'Yes' or advance == 'YES' or advance == 'yes':
                timevar += 3
                swvelocity = array2[timevar, 0]
                while swvelocity < -900 and endearly:
                    timevar += 3
                    swvelocity = array2[timevar, 0]
                    if timevar - timevar_copy > 15:
                        endearly = 0
                if endearly == 0:
                    print ('Solar wind velocity data unavilible.')
            elif advance == 'N' or advance == 'n' or advance == 'No' or advance == 'NO' or advance == 'no':
                dontquit = 0
            else:
                advance = raw_input('Input not recognized. Try Solar Wind speed 1 min later? (y/n) ')
        
        #sat_position = array1[hour,0]
        #tb.dictree(cdffile)
    time_adj = (timevar - timevar_copy)/884.0*(24*60.0)    
    print "The velocity is "
    print swvelocity
    print 'The time adjustment is ' + str(time_adj) + ' min'
    print str(timevar) + ' min'
    print endearly 
    
    with pycdf.CDF(file_ko) as cdffile2:
        # print cdffile2
        array2 = cdffile2['V_GSM']
        print array2
        b = array2[:,0]
    
    a = list(range (0, 885))
    
   # plt.plot(a,b)
   # plt.show()
    
    
    