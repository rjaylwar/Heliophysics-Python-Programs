# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 17:29:28 2014

@author: rjaylward
"""

import os
import urllib2
from spacepy import pycdf
import math
import matplotlib.pyplot as plt
import numpy

inst_name = ['wi_k0_swe','wi_h0_mfi','wi_k0_3dp']
#probably shouln't have this golbally defined but it is just a lot easier this way

def cdfdate():
    year = input('Year: ')
    month = input('Month: ')
    day = input('Day: ')
    hour = input('Hour: ')    
    minute = input('Minute: ')
    seconds = input('Seconds: ')
    
    date = [year,month,day,hour,minute,seconds]

    print ' '    
    return date

def cdfnamer(date):

    file_end = str(date[0]) + str(date[1]) + str(date[2]) + '.cdf' 
    
    have_cdf = [0,0,0]
    a = 0
    
    for instrument in inst_name:
        file_name = instrument + file_end
        
        try:
            cdftest = pycdf.CDF(file_name)
        except:
            print instrument + " File not found. Preparing to download..."
        else:
            print "you already have this file"
            have_cdf[a] = 1
            cdftest.close()
        a += 1 
    
    return have_cdf
        
def cdfdownloader(date,have_cdf):
    
    version = [1,2,3,4,5]
    count_a = 0
    v_1 = 1
    v_5 = 5
    sweko_url = 'http://cdaweb.sci.gsfc.nasa.gov/sp_phys/data/wind/swe/swe_k0/' + str(date[0]) + '/' + 'wi_k0_swe_' + str(date[0]) + str(date[1]) + str(date[2]) + '_v0' #1.cdf
    mfiho_url = 'http://cdaweb.sci.gsfc.nasa.gov/sp_phys/data/wind/mfi/mfi_h0/' + str(date[0]) + '/' + 'wi_h0_mfi_' + str(date[0]) + str(date[1]) + str(date[2]) + '_v0' #5.cdf
    tdpko_url = 'http://cdaweb.sci.gsfc.nasa.gov/sp_phys/data/wind/3dp/3dp_k0/' + str(date[0]) + '/' + 'wi_k0_3dp_' + str(date[0]) + str(date[1]) + str(date[2]) + '_v0' #1.cdf    
        
    
    urlist = [sweko_url, mfiho_url, tdpko_url]
    file_end = str(date[0]) + str(date[1]) + str(date[2]) + '.cdf'
    
    
    for url in urlist:
        file_name = inst_name[count_a] + file_end
        if have_cdf[count_a] == 0:
            for v in version:
                try: 
                    f = urllib2.urlopen(url + str(v) + '.cdf')
                    f_cdf = open(file_name, 'w')
                    f_cdf.write(f.read())
                    f_cdf.close() 
                    break 
                except urllib2.HTTPError as e:
                    print "An error has occured, the wrong version was selected" 
                    print e.code
                except urllib2.URLError:
                    print e.reason
            
        count_a += 1

    
def sw_avg_velocity(date):
    file_name = inst_name[0] + str(date[0]) + str(date[1]) + str(date[2]) + '.cdf' 
    timepercent = ((date[3]*3600 + date[4]*60 + date[5])/(24.*60*60))*884
    # this is for the k0 file, divides each day into interval of 884 time periods    
    
    timevar = int(math.floor(timepercent))
#    print timevar   
    timevarminus = timevar - 50 
    
    with pycdf.CDF(file_name) as cdffile1:
        # print cdffile2
        array1 = cdffile1['V_GSM']
#        print array1
        speed_vx = array1[timevar,0]

        speed_vx_array = array1[timevarminus:timevar,0]
        base_sum = 0     
        divby = 0
        
        for v in speed_vx_array:
            if v > -900:
                base_sum += v
                divby += 1
        
        print 'velocity'
        sw_avg_vel = base_sum / divby
        print sw_avg_vel
        return sw_avg_vel
        
def sw_position(date):
    file_name = inst_name[1] + str(date[0]) + str(date[1]) + str(date[2]) + '.cdf'

    with pycdf.CDF(file_name) as cdffile1:
        #print cdffile
        array1 = cdffile1['P1GSM']
        print 'position'
#        print array1[:,0]
        sat_position = array1[date[3],0]
#        print sat_position
        corrected_position = sat_position + ((array1[date[3]+1,0] - array1[date[3],0]) / 60.) * date[4]
        # Position is only updated every hour so this corrects for that getting a weighted average of the positions
        print corrected_position
    
        return corrected_position
        
def time_lag(sw_avg_vel, corrected_position, date):      
    
    min_lag = (((corrected_position) - 11)*(6378)/(sw_avg_vel))/60
    
    if date[4] > min_lag:
        date[4] += -min_lag
    elif date[3] > 0: 
        date[3] += -1
        sec = ((date[4] + 60 - min_lag) - math.floor(date[4] + 60 - min_lag))*60
        date[4] = int(math.floor(date[4] + 60 - min_lag))
        if date[5] + sec < 60:
            date[5] += sec
        else:
            seconds = date[5]
            date[4] += 1
            date[5] = seconds + sec - 1
    else:
        print "PROGRAM WAS NOT DESIGNED TO HANDLE THESE TIME PERIODS, DATA IS INVALID"
    
    date[5] = int(round(date[5]))
    print ('The time lag is -' + str(min_lag) + ' min')
    print date
    return date 
    
def sw_velocity(date_adj):
    file_name = inst_name[0] + str(date_adj[0]) + str(date_adj[1]) + str(date_adj[2]) + '.cdf' 
    timepercent = ((date_adj[3]*3600 + date_adj[4]*60 + date_adj[5])/(24.*60*60))*884
    # this is for the k0 file, divides each day into interval of 884 time periods    
    
    timevar = int(math.floor(timepercent))
#    print timevar    
    
    with pycdf.CDF(file_name) as cdffile1:
        # print cdffile1
        array1 = cdffile1['V_GSM']
        speed_vx = array1[timevar,0]
        print (str(speed_vx) + ' m/s')
    return speed_vx

def mag_field(date_adj):
    file_name = inst_name[1] + str(date_adj[0]) + str(date_adj[1]) + str(date_adj[2]) + '.cdf'
    
    with pycdf.CDF(file_name) as cdffile2:
        #print cdffile1
        array2 = cdffile2['BGSM']
#        print 'this is the ho file'
#        print array2[:,0]
        bx = array2[date_adj[4],0]
        by = array2[date_adj[4],1]
        bz = array2[date_adj[4],2]
        
        print ('bx = ' + str(bx))
        print ('by = ' + str(by))
        print ('bz = ' + str(bz))
        #tb.dictree(cdffile)
        
        mag_vector = [bx,by,bz]
#        print mag_vector
        return mag_vector 

def ion(date_adj):
    timepercent_ion = ((date_adj[3]*3600 + date_adj[4]*60 + date_adj[5])/(24.*60*60))*939
    timevar_ion = int(round(timepercent_ion))
    file_name = inst_name[2] + str(date_adj[0]) + str(date_adj[1]) + str(date_adj[2]) + '.cdf'
    
    with pycdf.CDF(file_name) as cdffile3:
#        print cdffile1
        
        array3 = cdffile3['ion_density']
#        print 'this is the ho file'
        ion_scalar = array3[timevar_ion]
        print 'Ion (scalar)'
        print ion_scalar
#        sat_position = array1[hour,0]
#        print ' '
#        print sat_position
#        print ' '
#        #tb.dictree(cdffile)

    return ion_scalar 

def main():
    date = cdfdate()
    have_cdf = cdfnamer(date)
    cdfdownloader(date,have_cdf)
    print" "
    sw_avg_vel = sw_avg_velocity(date)
    print" "
    corrected_position = sw_position(date)
    if corrected_position > 0 :
        print ('This program is not currently designed to handle the parameters of this day')
        print ('The satallite is in front of the earth, therefore the current time delay formula is wrong')
        print ' ' 
    else:
        print" "
        date_adj = time_lag(sw_avg_vel, corrected_position, date)
        print" "
        sw_velocity(date_adj)
        print" "
        mag_field(date_adj)
        print" "
        ion(date_adj)
        print ' ' 
    continu = raw_input('Continue? (y/n): ')
    if continu == 'y' or continu == 'y ' or continu == 'Y' or continu == 'yes' or continu == 'Yes' or continu == 'Yes' or continu == '1' or continu == 1:
        main()
    
if __name__ == "__main__":
	main()
    
    