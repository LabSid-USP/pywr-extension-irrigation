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


mymodel = Model.load("D:/Git/pywr-extension-irrigation1/examples/Rede_mensal.json")
mymodel.run()

