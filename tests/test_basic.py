# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 14:49:15 2021

@author: ewanh
"""

import unittest
import sys
sys.path.append("..")
from intersectionCheckerModule import intersectionClass

import numpy as np

class IntersectTestCase(unittest.TestCase):
    def setUp(self):
        '''
        initialise arrays of 5 scenarios:
            1) triangle fully enclosed by circle
            2) triangle intersecting circle (2 edges)
            3) triangle outside of circle whose projected edges don't intersect the circle
            4) triangle outside of circle whose projected edge does intersect the circle 
            5) triangle surrounds circle'''
        self.scenarionumber=5
        self.polygonptsArray=[[[5,0],[0,0],[0,5]],[[5,0],[15,0],[15,15]],[[5,10.1],[20,10.1],[20,5]],[[5,9],[20,10],[20,5]],[[-50,-50],[-50,50],[50,0]]]
        self.circleptArray=np.repeat([0,0],self.scenarionumber)
        self.radii=np.repeat(10,self.scenarionumber)
        self.pairs=[]
        
        for case in range(5):
            self.pairs.append(intersectionClass.IntersectionPair(polygonpts=self.polygonptsArray[case],circlept=self.circleptArray[case],r=self.radii[case]))

    def test_summary(self):
        summaries=['Triangle is Entirely Enclosed by Circle','2/3 Line Segments Intersect Circle','Triangle and circle are separate','Triangle and circle are separate','Circle is Fully Enclosed by Triangle']
        for i in range(self.scenarionumber):
            self.assertEqual(summaries[i],self.pairs[i].summary,'incorrect summary for case {}'.format(i))
   
if __name__=='__main__':
   IntersectTestCase()
   unittest.main()
