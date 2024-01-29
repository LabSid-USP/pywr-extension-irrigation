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




class WaterStressCoefficient(Parameter):
    """
    Water stress coefficient parameter calculated from current volume

    Parameters
    ----------
    node: Node
        Soil Reservoir node to provide input volume values to interpolation calculation
    CC: float
        Field Capacity of Soil (%).
    PMP : float
        Wilting Point of Soil (%).
    dg: float
       Bulk Densityof Soil (g/cm3).
    zr : float
        Depth Rootzone of Soil (cm).
    arr: float
        Irrigated Area (m2)
    
    "uin": float
        Initial soil Moisture (%).
    """

    def __init__(self, model, node, **kwargs):
        super(WaterStressCoefficient, self).__init__(
            model, **kwargs
        )
        self._node = node
        self.cc = self._node.FC
        self.pmp=self._node.WP
        self.dg=self._node.dg
        self.zr=self._node.Zr
        self.arr=self._node.Airr
        self.uin=self._node.Uin
        self.initial_value = self._node.initial_volume

    def setup(self):
        super().setup()
        self.cc = self._node.FC
        self.pmp=self._node.WP
        self.dg=self._node.dg
        self.zr=self._node.Zr
        self.arr=self._node.Airr
        self.uin=self._node.Uin
        self.initial_value = self._node.initial_volume      
        

                    
    def value(self, timestep, scenario_index):
        timestep = self.model.timestepper.current
        if timestep== 0:
            CAA1= ((self.uin-self.pmp)/100)*self.dg*self.zr*10
            CTA1=((self.cc-self.pmp)/100)*self.dg*self.zr*10
            self.z=(math.log((CAA1+1)))/(math.log((CTA1+1)))
        else:
            AS_ini_1=((((self._node.volume[scenario_index.global_id]))/self._node.Airr.get_value(scenario_index))*1000)/self._node.days.get_value(scenario_index)
            Uin_1=((AS_ini_1*100)/(self._node.Zr.get_value(scenario_index)*10*self._node.dg.get_value(scenario_index)))
            if Uin_1-self._node.WP.get_value(scenario_index)<10e-14:
              Uin=self._node.WP.get_value(scenario_index)
            else:
              Uin= Uin_1
            CAA= ((Uin-self._node.WP.get_value(scenario_index))/100)*self._node.dg.get_value(scenario_index)*self._node.Zr.get_value(scenario_index)*10
            CTA=((self._node.FC.get_value(scenario_index)-self._node.WP.get_value(scenario_index))/100)*self._node.dg.get_value(scenario_index)*self._node.Zr.get_value(scenario_index)*10
            self.z=(math.log((CAA+1)))/(math.log((CTA+1)))
        return self.z

    

    @classmethod
    def load(cls, model, data):
        node = model.nodes[data.pop("node")]
          
        
        return cls(model, node, **data)


WaterStressCoefficient.register()
