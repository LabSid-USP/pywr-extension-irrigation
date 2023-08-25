import os
import sys
import datetime
import pywr
import pandas as pd
from pywr.core import Timestepper
from pywr.core import Model, Input, Output
from pywr.core import *
from pywr.nodes import *
from pywr.recorders import NumpyArrayNodeRecorder, ParameterRecorder, Recorder, NumpyArrayParameterRecorder
from pywr.model import Model
from pywr.nodes import Node, Link, Output

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pywr_ext_irrigation.modules import AquiferWithoutKeatingOutflows
from pywr_ext_irrigation.modules import SoilReservoir
from pywr_ext_irrigation.parameters import Evapotranspiration
from pywr_ext_irrigation.parameters import PreliminarIrrigatedVolume
from pywr_ext_irrigation.parameters import WaterStressCoefficient


mymodel = Model.load("D:/Git/pywr-extension-irrigation/examples/rede_bauru_fim.json")




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


try:
        r34 = mymodel.recorders["par1"]
        #r34 = mymodel.recorders["vol2"]
except KeyError:
        print("Not found")
else:
         def22=pd.DataFrame(r34.data)
         print(r34.data)
