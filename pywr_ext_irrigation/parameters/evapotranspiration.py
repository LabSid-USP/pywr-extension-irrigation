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

class Evapotranspiration(Parameter):

    """
    Actual evapotranspiration
    Parameters
    ----------
    Etp: Parameter
        Potential Evapotranspiration (mm)
    Kc: Parameter
        Monthly Profile Crop Coefficient (array).        
    node: Parameter
        Soil reservoir associated.
        
    """
    def __init__(self, model, Etp, Kc, node, **kwargs):
        super().__init__(model, **kwargs)
        self.parameters = Etp
        self.kc=Kc
        self._node = node

         
            
    def value(self, timestep, scenario_index):
        Etp_ini = (self.parameters.get_value(scenario_index))*(1/self._node.days.get_value(scenario_index))
        kc_ref = self.kc.get_value(scenario_index)
        Et_ini= Etp_ini*kc_ref
        if Et_ini<=0:
            Et=0.0
        else:
            Et=Et_ini
        
        return Et

    @classmethod
    def load(cls, model, data):
        Etp = load_parameter(model,data.pop("etp"))
        Kc = load_parameter(model,data.pop("kc"))
        node = model.nodes[data.pop("node")]
        return cls(model, Etp, Kc, node, **data)

Evapotranspiration.register()


class Evapotranspiration_soil(Parameter):

    """
    Actual evapotranspiration
    Parameters
    ----------
    Etp: Parameter
        Potential Evapotranspiration (mm)
    Airr: float
        Irrigated Area (m2)
    Kc: Parameter
        Monthly Profile Crop Coefficient (array).
    Ks : Parameter
        Water Stress Coefficient 
        
    """
    def __init__(self, model, Etp, Kc, Ks, node, **kwargs):
        super().__init__(model, **kwargs)
        self.parameters = Etp
        self.ks = Ks
        self.kc=Kc
        self._node = node
    
       
            
    def value(self, timestep, scenario_index):
        Etp_ini = self.parameters.get_value(scenario_index)*(1/self._node.days.get_value(scenario_index))
        kc_ref = self.kc.get_value(scenario_index)
        ks_ref = self.ks.get_value(scenario_index)
        Et_ini= Etp_ini*kc_ref*ks_ref
        if Et_ini<=0:
            Et=0.0
        else:
            Et=Et_ini*0.001*self._node.Airr.get_value(scenario_index)*self._node.days.get_value(scenario_index)
        
        return Et

    @classmethod
    def load(cls, model, data):
        Etp = load_parameter(model,data.pop("etp"))
        Kc = load_parameter(model,data.pop("kc"))
        Ks = load_parameter(model,data.pop("ks"))
        node = model.nodes[data.pop("node")]
        return cls(model, Etp, Kc, Ks, node, **data)

Evapotranspiration_soil.register()
