import dataclasses
import pywr
import datetime 
import math

from pywr.core import Timestepper
from pywr.core import Model, Input, Output
from pywr.core import *
from pywr.nodes import *
from pywr.parameters import control_curves
from pywr.recorders import NumpyArrayNodeRecorder
import pandas as pd
import numpy as np
from pandas import read_csv


from pywr.nodes import Node, Link, Output, Storage
from pywr.domains import *
from pywr.parameters import Parameter

from pywr.parameters import Parameter

class PreliminarIrrigatedVolume(Parameter):
    """
    Preliminar Irrigated Volume
    Parameters
    ----------
    Eta: Parameter
        Actual Evapotranspiration (Mm3)
    Prec: Parameter
        Monthly Precipitation (Mm3).
    AS : Node
        Soil Reservoir node to provide input volume values to calculation
        
    """
    def __init__(self, model, Eta, Prec, AS, f, ef, **kwargs):
        super().__init__(model, **kwargs)
        self.parameters = Eta
        self.Prec=Prec
        self.AS=AS
        self.f=f
        self.ef=ef
            
    def value(self, timestep, scenario_index):
        Eta_ini = self.parameters.get_value(scenario_index)
        Prec_ini = self.Prec.get_value(scenario_index)
        AS_ini=self.AS.volume[scenario_index.global_id]
        if Eta_ini-Prec_ini-((AS_ini*4)*self.f)<=0:
            total=0.0
        else:
            total=(Eta_ini-Prec_ini-((AS_ini*4)*self.f))/self.ef
        
     
        return total


        
        
    @classmethod
    def load(cls, model, data):
        Eta = load_parameter(model,data.pop("eta"))
        Prec = load_parameter(model,data.pop("prec"))
        AS = model.nodes[data.pop("AS")]
        f = data.pop("f")
        ef=data.pop("efic")
        return cls(model, Eta, Prec, AS,f, ef, **data)

PreliminarIrrigatedVolume.register()

