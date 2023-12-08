from pyomo.environ import ConcreteModel, SolverFactory

from idaes.core import FlowsheetBlock, FlowDirection
from idaes.core.util.model_statistics import degrees_of_freedom as dof
from idaes.core.initialization.block_triangularization import (
    BlockTriangularizationInitializer,
)
from idaes.core.initialization import InitializationStatus

from SolventExtraction import SolventExtraction

from REEAqdistribution import REESolExAqParameters
from REEOgdistribution import REESolExOgParameters

m = ConcreteModel()
m.fs = FlowsheetBlock(dynamic=False)
m.fs.prop_a = REESolExAqParameters()
m.fs.prop_o = REESolExOgParameters()

m.fs.solex = SolventExtraction(
    number_of_finite_elements=3,
    dynamic=False,
    aqueous_stream={
        "property_package": m.fs.prop_a,
        "flow_direction": FlowDirection.forward,
        "has_energy_balance": False,
        "has_pressure_balance": False,
    },
    organic_stream={
        "property_package": m.fs.prop_o,
        "flow_direction": FlowDirection.backward,
        "has_energy_balance": False,
        "has_pressure_balance": False,
    },
)


m.fs.solex.mscontactor.aqueous_inlet_state[0].conc_mass_comp["Al"].fix(820)
m.fs.solex.mscontactor.aqueous_inlet_state[0].conc_mass_comp["Ca"].fix(5230)
m.fs.solex.mscontactor.aqueous_inlet_state[0].conc_mass_comp["Fe"].fix(270)
m.fs.solex.mscontactor.aqueous_inlet_state[0].conc_mass_comp["Sc"].fix(209.31)
m.fs.solex.mscontactor.aqueous_inlet_state[0].conc_mass_comp["Y"].fix(637.74)
m.fs.solex.mscontactor.aqueous_inlet_state[0].conc_mass_comp["La"].fix(2032.77)
m.fs.solex.mscontactor.aqueous_inlet_state[0].conc_mass_comp["Ce"].fix(4516.13)
m.fs.solex.mscontactor.aqueous_inlet_state[0].conc_mass_comp["Pr"].fix(756.64)
m.fs.solex.mscontactor.aqueous_inlet_state[0].conc_mass_comp["Nd"].fix(2047.85)
m.fs.solex.mscontactor.aqueous_inlet_state[0].conc_mass_comp["Sm"].fix(369.1)
m.fs.solex.mscontactor.aqueous_inlet_state[0].conc_mass_comp["Gd"].fix(174.38)
m.fs.solex.mscontactor.aqueous_inlet_state[0].conc_mass_comp["Dy"].fix(101.12)

m.fs.solex.mscontactor.aqueous_inlet_state[0].flow_vol.fix(4.4)

m.fs.solex.mscontactor.organic_inlet_state[0].conc_mass_comp["Al"].fix(7.54e-10)
m.fs.solex.mscontactor.organic_inlet_state[0].conc_mass_comp["Ca"].fix(4.955e-9)
m.fs.solex.mscontactor.organic_inlet_state[0].conc_mass_comp["Fe"].fix(1.491e-7)
m.fs.solex.mscontactor.organic_inlet_state[0].conc_mass_comp["Sc"].fix(321.34)
m.fs.solex.mscontactor.organic_inlet_state[0].conc_mass_comp["Y"].fix(5.67e-6)
m.fs.solex.mscontactor.organic_inlet_state[0].conc_mass_comp["La"].fix(1.78e-05)
m.fs.solex.mscontactor.organic_inlet_state[0].conc_mass_comp["Ce"].fix(4.019e-5)
m.fs.solex.mscontactor.organic_inlet_state[0].conc_mass_comp["Pr"].fix(6.73e-6)
m.fs.solex.mscontactor.organic_inlet_state[0].conc_mass_comp["Nd"].fix(1.82e-5)
m.fs.solex.mscontactor.organic_inlet_state[0].conc_mass_comp["Sm"].fix(3.285e-6)
m.fs.solex.mscontactor.organic_inlet_state[0].conc_mass_comp["Gd"].fix(1.55e-6)
m.fs.solex.mscontactor.organic_inlet_state[0].conc_mass_comp["Dy"].fix(9e-7)

m.fs.solex.mscontactor.organic_inlet_state[0].flow_vol.fix(62.01)

print(dof(m))

# Initializing of the model

initializer = BlockTriangularizationInitializer()
initializer.initialize(m.fs.solex)
assert initializer.summary[m.fs.solex]["status"] == InitializationStatus.Ok

# Solving of the model

solver = SolverFactory("ipopt")
solver.solve(m, tee=True)

# Final organic outlet display
m.fs.solex.mscontactor.organic[0, 1].conc_mass_comp.display()

# Final aqueous outlets display
m.fs.solex.mscontactor.aqueous[0, 3].conc_mass_comp.display()
