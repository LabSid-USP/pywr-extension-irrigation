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

from .soil_storage import SoilStorage

class SoilReservoir(RiverDomainMixin, SoilStorage):
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
        super(SoilReservoir, self).__init__(model, *args, **kwargs)
        
