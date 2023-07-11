

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
from pywr.model import Model
from pywr.nodes import Node, Link, Output
import os



mymodel = Model.load("Rede.json")

mymodel.run()
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
