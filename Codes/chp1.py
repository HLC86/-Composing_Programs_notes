#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:08:25 2022

@author: hongliangchai
"""

from urllib.request import urlopen
shakespeare = urlopen('http://composingprograms.com/shakespeare.txt')

words = set(shakespeare.read().decode().split())
{w for w in words if len(w) == 6 and w[::-1] in words}

#%%

