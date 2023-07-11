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

class VIRN(Parameter):
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

VIRN.register()


class Evapotranspiration(Parameter):

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
        Etp_ini = self.parameters.get_value(scenario_index)
        kc_ref = self.kc.get_value(scenario_index)
        ks_ref = self.ks.get_value(scenario_index)
        Et_ini= Etp_ini*kc_ref*ks_ref
        if Et_ini<=0:
            Et=0.0
        else:
            Et=Et_ini* self._node.Airr.get_value(scenario_index)*0.001*0.000001
        
        return Et

    @classmethod
    def load(cls, model, data):
        Etp = load_parameter(model,data.pop("etp"))
        Kc = load_parameter(model,data.pop("kc"))
        Ks = load_parameter(model,data.pop("ks"))
        node = model.nodes[data.pop("node")]
        return cls(model, Etp, Kc, Ks, node, **data)

Evapotranspiration.register()



class Ks_calcp(Parameter):
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
        super(Ks_calcp, self).__init__(
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
            AS_ini=self._node.volume[scenario_index.global_id]
            Uin=(AS_ini*100000000)/(self._node.Zr.get_value(scenario_index)*10*0.001*self._node.Airr.get_value(scenario_index))+self._node.WP.get_value(scenario_index)
            CAA= ((Uin -self._node.WP.get_value(scenario_index))/100)*self._node.dg.get_value(scenario_index)*self._node.Zr.get_value(scenario_index)*10
            CTA=((self._node.FC.get_value(scenario_index)-self._node.WP.get_value(scenario_index))/100)*self._node.dg.get_value(scenario_index)*self._node.Zr.get_value(scenario_index)*10
            self.z=(math.log((CAA+1)))/(math.log((CTA+1)))
        return self.z


    @classmethod
    def load(cls, model, data):
        node = model.nodes[data.pop("node")]
          
        
        return cls(model, node, **data)


Ks_calcp.register()