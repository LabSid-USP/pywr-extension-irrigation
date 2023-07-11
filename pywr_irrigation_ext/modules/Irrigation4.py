import pywr
import datetime
from pywr import parameters
from pywr.core import Timestepper
from pywr.core import Model, Input, Output
from pywr.core import *
from pywr.nodes import *
from pywr.parameters import control_curves
from pywr.recorders import NumpyArrayNodeRecorder
import pandas as pd
import numpy as np
from pandas import read_csv
from pywr import _core
from pywr._core import Node as BaseNode
from pywr._core import BaseInput, BaseLink, BaseOutput, StorageInput, StorageOutput

from pywr.nodes import Node, Link, Output, Storage
from pywr.domains import *
from pywr.nodes import Domain, Input, Link, Storage, PiecewiseLink, MultiSplitLink
from pywr.parameters import (
    pop_kwarg_parameter,
    ConstantParameter,
    Parameter,
    load_parameter,
    MonthlyProfileParameter,
)
from pywr.parameters.control_curves import ControlCurveParameter



class Storage2(Loadable, Drawable, Connectable, _core.Storage, metaclass=NodeMeta):
    """A generic storage Node

    In terms of connections in the network the Storage node behaves like any
    other node, provided there is only 1 input and 1 output. If there are
    multiple sub-nodes the connections need to be explicit about which they
    are connecting to. For example:

    >>> storage(model, 'reservoir', num_outputs=1, num_inputs=2)
    >>> supply.connect(storage)
    >>> storage.connect(demand1, from_slot=0)
    >>> storage.connect(demand2, from_slot=1)

    The attribtues of the sub-nodes can be modified directly (and
    independently). For example:

    >>> storage.outputs[0].max_flow = 15.0

    If a recorder is set on the storage node, instead of recording flow it
    records changes in storage. Any recorders set on the output or input
    sub-nodes record flow as normal.

    Parameters
    ----------
    model : Model
        Model instance to which this storage node is attached.
    name : str
        The name of the storage node.
    num_inputs, num_outputs : integer (optional)
        The number of input and output nodes to create internally. Defaults to 1.
    min_volume : float (optional)
        The minimum volume of the storage. Defaults to 0.0.
    max_volume : float, Parameter (optional)
        The maximum volume of the storage. Defaults to 0.0.
    initial_volume, initial_volume_pc : float (optional)
        Specify initial volume in either absolute or proportional terms. Both are required if `max_volume`
        is a parameter because the parameter will not be evaluated at the first time-step. If both are given
        and `max_volume` is not a Parameter, then the absolute value is ignored.
    cost : float, Parameter (optional)
        The cost of net flow in to the storage node. I.e. a positive cost penalises increasing volume by
        giving a benefit to negative net flow (release), and a negative cost penalises decreasing volume
        by giving a benefit to positive net flow (inflow).
    area, level : float, Parameter (optional)
        Optional float or Parameter defining the area and level of the storage node. These values are
        accessible through the `get_area` and `get_level` methods respectively.
    """
    __parameter_attributes__ = ('cost', 'min_volume', 'max_volume', 'level', 'area','Uin','dg','Zr','Airr','WP','FC')
    __parameter_value_attributes__ = ('initial_volume', )


    def __init__(self, model, name, outputs=1, inputs=1, *args, **kwargs):

        min_volume = pop_kwarg_parameter(kwargs, 'min_volume', 0.0)
        if min_volume is None:
            min_volume = 0.0
        max_volume = pop_kwarg_parameter(kwargs, 'max_volume', 0.0)
        initial_volume = kwargs.pop('initial_volume', None)
        initial_volume_pc = kwargs.pop('initial_volume_pc', None)
        cost = pop_kwarg_parameter(kwargs, 'cost', 0.0)
        level = pop_kwarg_parameter(kwargs, 'level', None)
        area = pop_kwarg_parameter(kwargs, 'area', None)
        Uin = pop_kwarg_parameter(kwargs,'Uin', 0.0)
        dg =pop_kwarg_parameter(kwargs, 'dg', 0.0)
        Zr = pop_kwarg_parameter(kwargs, 'Zr', 0.0)
        Airr = pop_kwarg_parameter(kwargs, 'Airr', 0.0)
        WP =pop_kwarg_parameter(kwargs, 'WP', 0.0)
        FC =pop_kwarg_parameter(kwargs,'FC', 0.0)
        
      

        super(Storage2, self).__init__(model, name, **kwargs)

        self.outputs = []
        for n in range(0, outputs):
            self.outputs.append(StorageOutput(model, name="[output{}]".format(n), parent=self))

        self.inputs = []
        for n in range(0, inputs):
            self.inputs.append(StorageInput(model, name="[input{}]".format(n), parent=self))


        self.Uin = Uin
        self.dg = dg
        self.Zr = Zr
        self.Airr = Airr
        self.WP = WP
        self.FC = FC
        self.cost = cost
        self.level = level
        self.area = area
        self.min_volume = min_volume
        self.max_volume = max_volume
        self.initial_volume = initial_volume

        
        # StorageOutput and StorageInput are Cython classes, which do not have
        # NodeMeta as their metaclass, therefore they don't get added to the
        # model graph automatically.
        for node in self.outputs:
            self.model.graph.add_node(node)
        for node in self.inputs:
            self.model.graph.add_node(node)

    def iter_slots(self, slot_name=None, is_connector=True, all_slots=False):
        if is_connector:
            if not self.inputs:
                raise StopIteration
            if slot_name is None:
                if all_slots or len(self.inputs) == 1:
                    for node in self.inputs:
                        yield node
                else:
                    raise ValueError("Must specify slot identifier.")
            else:
                try:
                    yield self.inputs[slot_name]
                except IndexError:
                    raise IndexError('{} does not have slot: {}'.format(self, slot_name))
        else:
            if not self.outputs:
                raise StopIteration
            if slot_name is None:
                if all_slots or len(self.outputs) == 1:
                    for node in self.outputs:
                        yield node
                else:
                    raise ValueError("Must specify slot identifier.")
            else:
                yield self.outputs[slot_name]

    def check(self):        
        pass  # TODO


    def setup(self, model):
        def _get_value(parameter):
            return parameter.get_constant_value() if isinstance(parameter, Parameter) else parameter
        self.min_volume = ((((_get_value(self.WP))/100)*_get_value(self.dg)*_get_value(self.Zr)*10*0.001)*_get_value(self.Airr))
        self.max_volume = ((((_get_value(self.FC)-_get_value(self.WP))/100)*_get_value(self.dg)*_get_value(self.Zr)*10*0.001)*_get_value(self.Airr))      
        #self.initial_volume = ((((_get_value(self.Uin)-_get_value(self.WP))/100)*_get_value(self.dg)*_get_value(self.Zr)*10*0.001)*_get_value(self.Airr))
            
        super().setup(model)

    def __repr__(self):
        return '<{} "{}">'.format(self.__class__.__name__, self.name)

DEFAULT_RIVER_DOMAIN = Domain(name="river", color="#33CCFF")

class Soil_Reservoir(RiverDomainMixin, Storage2):
    """A reservoir node with control curve.

    The Reservoir is a subclass of Storage with additional functionality to provide a
    simple control curve. The Reservoir has above_curve_cost when it is above its curve
    and the user defined cost when it is below. Typically the costs are negative
    to represent a benefit of filling the reservoir when it is below its curve.
    """

    def __init__(self, model, *args, **kwargs):
        """

        Keywords:
            control_curve - A Parameter object that can return the control curve position,
                as a percentage of fill, for the given timestep.
        """
        control_curve = pop_kwarg_parameter(kwargs, "control_curve", None)
        above_curve_cost = kwargs.pop("above_curve_cost", None)
        cost = kwargs.pop("cost", 0.0)
        if above_curve_cost is not None:
            if control_curve is None:
                # Make a default control curve at 100% capacity
                control_curve = ConstantParameter(model, 1.0)
            elif not isinstance(control_curve, Parameter):
                # Assume parameter is some kind of constant and coerce to ConstantParameter
                control_curve = ConstantParameter(model, control_curve)

            if not isinstance(cost, Parameter):
                # In the case where an above_curve_cost is given and cost is not a Parameter
                # a default cost Parameter is created.
                kwargs["cost"] = ControlCurveParameter(
                    model, self, control_curve, [above_curve_cost, cost]
                )
            else:
                raise ValueError(
                    "If an above_curve_cost is given cost must not be a Parameter."
                )
        else:
            # reinstate the given cost parameter to pass to the parent constructors
            kwargs["cost"] = cost
        super(Soil_Reservoir, self).__init__(model, *args, **kwargs)
        



