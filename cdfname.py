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

def cdfname():

    file_ko = 'wi_k0_swe' + str(year) + str(month) + str(day) + '.cdf'
    
    have_cdf = 0
    
    try:
        cdftest = pycdf.CDF(file_ko)
    except:
        print "Error: can\'t find file or read data"
    else:
        print "you already have this file"
        have_cdf = 1
        cdftest.close()