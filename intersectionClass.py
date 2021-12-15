# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 14:49:15 2021

@author: ewanh
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class IntersectionPair():
    '''
    This class determines the relationship between a polygon and a circle.
    There are 4 possible resulting summaries
    - circle encloses polygon
    - polygon and circle intersect
    - polygon encloses circle
    - polygon is outside of circle
    The polygon must be convex.
    inputs: coordinates of polygon verteces (as list of x,y pairs), centre position of circle (as x,y pair), circle radius
    '''
    def __init__(self,**kwargs):
        if 'polygonpts' in kwargs:
            self.polygonpts=kwargs['polygonpts']
        if 'circlept' in kwargs:
            self.circlept=kwargs['circlept']
        if 'r' in kwargs:
            self.r=kwargs['r']
        length=len(self.polygonpts)
        lines=np.empty([length,2])
        summary=''
        intersecting=np.empty (length, dtype =bool)
        outside=np.empty (length, dtype =bool)
        inside=np.empty (length, dtype =bool)
        self.xproducts=np.zeros(length)
      
        for i in range(0,length):  
            #normalise the magnitude of each line
            lines[i]=np.subtract(self.polygonpts[i],self.polygonpts[((i+2)%length)-1])
            lines[i][:]=lines[i][:]/np.linalg.norm(lines[i])
            if (np.linalg.norm(self.polygonpts[i]-self.circlept)>self.r)^(np.linalg.norm(self.polygonpts[((i+2)%length)-1]-self.circlept)>self.r):
                intersecting[i]=True
                outside[i]=False
                inside[i]=False
            else:
                if np.linalg.norm(self.polygonpts[i]-self.circlept)>self.r:
                    if ((abs(np.cross(lines[i],self.polygonpts[i]-self.circlept))<self.r)& (np.dot(self.polygonpts[i]-self.circlept,lines[i])* np.dot(self.polygonpts[((i+2)%length)-1]-self.circlept,lines[i])<0)):
                        intersecting[i]=True
                        outside[i]=False
                        inside[i]=False
                    else:
                        #mark edge as outside circle
                        inside[i]=False
                        intersecting[i]=False
                        outside[i]=True
                        #record whether the line runs clockwise or anticlockwise to the circle centrepoint
                        self.xproducts[i]=np.cross(lines[i],self.polygonpts[i]-self.circlept)
                else:
                    outside[i]=False
                    intersecting[i]=False
                    inside[i]=True
                    
            if np.prod(inside):
                summary='Triangle is Entirely Enclosed by Circle'
                
            elif np.prod(outside):
                if np.all(self.xproducts>0)^np.all(self.xproducts<0):
                    summary='Circle is Fully Enclosed by Triangle'
                else:
                    summary='Triangle and circle are separate'
            else:
                summary='{}/{} Line Segments Intersect Circle'.format(int(np.sum(np.ones(length)[intersecting])),length)
         
            self.inside=inside
            self.intersecting=intersecting
            self.outside=outside
            self.summary=summary

    