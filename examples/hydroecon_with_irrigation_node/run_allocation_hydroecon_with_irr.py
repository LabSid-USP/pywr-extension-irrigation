import os
import sys
import pandas as pd
from pywr.model import Model

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

from pywr_ext_irrigation.modules import AquiferWithoutKeatingOutflows
from pywr_ext_irrigation.modules import SoilReservoir
from pywr_ext_irrigation.parameters import Evapotranspiration
from pywr_ext_irrigation.parameters import PreliminarIrrigatedVolume
from pywr_ext_irrigation.parameters import WaterStressCoefficient

mymodel = Model.load(os.path.join(os.path.dirname(__file__), "hydroecon_with_irrigation_node.json"))
mymodel.run()

try:
        r1 = mymodel.recorders["def1"]
except KeyError:
        print("Not found")
else:
         def_1=pd.DataFrame(r1.data)
         print(r1.data)
         def_1.to_csv(os.path.join(os.path.dirname(__file__), "results/hydroecon_with_irr_def1.csv"), sep='\t')

try:
        r2 = mymodel.recorders["def2"]
except KeyError:
        print("Not found")
else:
         def_2=pd.DataFrame(r2.data)
         print(r2.data)
         def_2.to_csv(os.path.join(os.path.dirname(__file__), "results/hydroecon_with_irr_def2.csv"), sep='\t')

try:
        r3 = mymodel.recorders["def3"]
except KeyError:
        print("Not found")
else:
         def_3=pd.DataFrame(r3.data)
         print(r3.data)
         def_3.to_csv(os.path.join(os.path.dirname(__file__), "results/hydroecon_with_irr_def3.csv"), sep='\t')