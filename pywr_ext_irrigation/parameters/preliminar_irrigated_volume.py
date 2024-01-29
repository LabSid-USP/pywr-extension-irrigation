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
        self.cc = self.AS.FC
        self.pmp=self.AS.WP
        self.dg=self.AS.dg
        self.zr=self.AS.Zr
        self.arr=self.AS.Airr
        self.uin=self.AS.Uin
        self.initial_value = self.AS.initial_volume
        

    def setup(self):
        super().setup()
        self.cc = self.AS.FC
        self.pmp=self.AS.WP
        self.dg=self.AS.dg
        self.zr=self.AS.Zr
        self.arr=self.AS.Airr
        self.uin=self.AS.Uin
        self.initial_value = self.AS.initial_volume   
        self.max_volume=  self.AS.max_volume
        
        
            
    def value(self, timestep, scenario_index):
        timestep = self.model.timestepper.current        
        Eta_ini = (self.parameters.get_value(scenario_index))
        Prec_ini = (self.Prec.get_value(scenario_index))*(1/self.AS.days.get_value(scenario_index))
        CTA=((self.AS.FC.get_value(scenario_index)-self.AS.WP.get_value(scenario_index))/100)*self.AS.dg.get_value(scenario_index)*self.AS.Zr.get_value(scenario_index)*10
        if timestep== 0:
            total=0
            CAA1= ((self.uin-self.AS.WP.get_value(scenario_index))/100)*self.AS.dg.get_value(scenario_index)*self.AS.Zr.get_value(scenario_index)*10
            ks=(math.log((CAA1+1)))/(math.log((CTA+1)))
            Eta_fim=Eta_ini*ks
            IRN= Eta_fim-Prec_ini-(CAA1*self.f)
            if IRN + (CAA1) > (CTA)*self.f:
                IRN= (CTA)-(CAA1)
            else:
                IRN=IRN
                
            ITN=(IRN/self.ef)*(self.AS.days.get_value(scenario_index))
            
            if IRN<=0:
                total=0
            else:
                total=(ITN*0.001*self.AS.Airr.get_value(scenario_index))
            
        else:
            total = 0
            AS_ini_1=(((self.AS.volume[scenario_index.global_id])/self.AS.Airr.get_value(scenario_index))*1000)/self.AS.days.get_value(scenario_index)
            Uin_1=((AS_ini_1*100)/(self.AS.Zr.get_value(scenario_index)*10*self.AS.dg.get_value(scenario_index)))
            if Uin_1-self.AS.WP.get_value(scenario_index)<10e-14:
              Uin=self.AS.WP.get_value(scenario_index)
            else:
              Uin= Uin_1
            CAA1= ((Uin-self.AS.WP.get_value(scenario_index))/100)*self.AS.dg.get_value(scenario_index)*self.AS.Zr.get_value(scenario_index)*10
            ks=(math.log((CAA1+1)))/(math.log((CTA+1)))
            Eta_fim=Eta_ini*ks
            IRN= Eta_fim-Prec_ini-(CAA1*self.f)
            if IRN<=0:
                total=0                
            else: 
             if IRN + (CAA1) > (CTA)*self.f:
                IRN= (CTA)-(CAA1)
             else:
                IRN=IRN
                
             ITN=(IRN/self.ef)*(self.AS.days.get_value(scenario_index))
             total=(ITN*0.001*self.AS.Airr.get_value(scenario_index))
            
     

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

