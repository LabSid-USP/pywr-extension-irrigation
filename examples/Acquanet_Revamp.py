

"""Revamp."""

__author__ = "LabSid PHA EPUSP"
__copyright__ = "Copyright 2020-2021, LabSid PHA EPUSP"
__license__ = "GPL"
__date__ = "2022-01-05"
__version__ = "0.1.0"



# Importing  functions

from modules.Irrigation4 import *
from parameters.SoilReservoir import *
from modules.aquifer import *




import pywr
import datetime
from pywr.core import Timestepper
from pywr.core import Model, Input, Output
from pywr.core import *
from pywr.nodes import *
from pywr.recorders import NumpyArrayNodeRecorder, ParameterRecorder, Recorder, NumpyArrayParameterRecorder
import pandas as pd
import numpy as np
from pandas import read_csv
from pywr.model import Model
from pywr.nodes import Node, Link, Output
from pcraster import *
import os
import configparser
import numpy as np
import openpyxl
from openpyxl import load_workbook
import pandas as pd
from pcraster.framework import dynamicBase
from pcraster.framework import *
from pcraster import *
import pcraster as pcr

configFile = "D:/ACQUANET/Artigo/17.ini"
# Leitura de arquivo config.ini
config = configparser.ConfigParser()
config.read(configFile)
outpath = config.get('FILES', 'output')
flag_sub= config.getboolean('ALLOCATION', 'Flag_sub')

#mymodel = Model.load("D:/ACQUANET/Artigo/rede_IRRIGACAO.json")
mymodel = Model.load("D:/ACQUANET/Artigo/rodaks.json")
mymodel.run()
if config.getboolean('ALLOCATION', 'Flag_irri'):   
    try:
        r1 = mymodel.nodes["Rsl_1"]
    except KeyError:
        print("Not found")
    else:
        nam1=(f"name: {r1.name}")
        min_volum1=((r1.min_volume))
        init_vo1=((r1.initial_volume))
        maxvol1=((r1.max_volume))
        uin1=((r1.Uin.get_constant_value()))
        dg1=((r1.dg.get_constant_value()))
        zr1=((r1.Zr.get_constant_value()))
        airr1=((r1.Airr.get_constant_value()))
        wp1=((r1.WP.get_constant_value()))
        fc1=((r1.FC.get_constant_value()))
        
        print(nam1,min_volum1,init_vo1,maxvol1,uin1,dg1,airr1,wp1,fc1)
        
    try:
        r2 = mymodel.nodes["Rsl_2"]
    except KeyError:
        print("Not found")
    else:
        nam2=(f"name: {r2.name}")
        min_volum2=((r2.min_volume))
        init_vo2=((r2.initial_volume))
        maxvol2=((r2.max_volume))
        uin2=((r2.Uin.get_constant_value()))
        dg2=((r2.dg.get_constant_value()))
        zr2=((r2.Zr.get_constant_value()))
        airr2=((r2.Airr.get_constant_value()))
        wp2=((r2.WP.get_constant_value()))
        fc2=((r2.FC.get_constant_value()))
        print(nam2,min_volum2,init_vo2,maxvol2,uin2,dg2,airr2,wp2,fc2)

    try:
        r3 = mymodel.nodes["Rsl_3"]
    except KeyError:
        print("Not found")
    else:
        nam3=(f"name: {r3.name}")
        min_volum3=((r3.min_volume))
        init_vo3=((r3.initial_volume))
        maxvol3=((r3.max_volume))
        uin3=((r3.Uin.get_constant_value()))
        dg3=((r3.dg.get_constant_value()))
        zr3=((r3.Zr.get_constant_value()))
        airr3=((r3.Airr.get_constant_value()))
        wp3=((r3.WP.get_constant_value()))
        fc3=((r3.FC.get_constant_value()))

        print(nam3,min_volum3,init_vo3,maxvol3,uin3,dg3,airr3,wp3,fc3)
    try:
        r20 = mymodel.recorders["vol1"]
    except KeyError:
        print("Not found")
    else:
         def11=pd.DataFrame(r20.data)
         def11.to_csv('D:/ACQUANET/Artigo/vol1.csv', mode='a', index=False, header=False)
         print("voluem")
         print(r20.data)
    try:
        r21 = mymodel.recorders["vol2"]
    except KeyError:
        print("Not found")
    else:
         def21=pd.DataFrame(r21.data)
         def21.to_csv('D:/ACQUANET/Artigo/vol2.csv', mode='a', index=False, header=False)

    try:
        r22 = mymodel.recorders["vol3"]
    except KeyError:
        print("Not found")
    else:
         def22=pd.DataFrame(r22.data)
         def22.to_csv('D:/ACQUANET/Artigo/vol3.csv', mode='a', index=False, header=False)
         
    try:
        r20 = mymodel.recorders["def1"]
    except KeyError:
        print("Not found")
    else:
         def11=pd.DataFrame(r20.data)
         def11.to_csv('D:/ACQUANET/Artigo/def1.csv', mode='a', index=False, header=False)
    try:
        r21 = mymodel.recorders["def2"]
    except KeyError:
        print("Not found")
    else:
         def21=pd.DataFrame(r21.data)
         def21.to_csv('D:/ACQUANET/Artigo/def2.csv', mode='a', index=False, header=False)

    try:
        r22 = mymodel.recorders["def3"]
    except KeyError:
        print("Not found")
    else:
         def22=pd.DataFrame(r22.data)
         def22.to_csv('D:/ACQUANET/Artigo/def3.csv', mode='a', index=False, header=False)


    try:
        r34 = mymodel.recorders["par1"]
    except KeyError:
        print("Not found")
    else:
        print("par1")
        print(r34.data)


    
if config.getboolean('ALLOCATION', 'Flag_sub'): 
    dfsub = pd.read_csv("D:/ACQUANET/Artigo/results.csv",  sep=",")
    dfsub.to_csv('D:/ACQUANET/Artigo/resultssubfim.csv', mode='a', index=False, header=False)
    
    

dfcapf = pd.read_csv("D:/ACQUANET/Artigo/resultscapt.csv",  sep=",")
dfcapf.to_csv('D:/ACQUANET/Artigo/resultscaptfim.csv', mode='a', index=False, header=False)

