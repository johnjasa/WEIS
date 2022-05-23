import openmdao.api as om

from wisdem.h2.hydrogen_group import HydrogenProduction

modeling_options = {}
modeling_options["WISDEM"] = {}
modeling_options["WISDEM"]["HydrogenProduction"] = {}
modeling_options["WISDEM"]["HydrogenProduction"]["read_in_power_signal"] = True
modeling_options["WISDEM"]["HydrogenProduction"]["power_filename"] = "weis_job_1.outb"

prob = om.Problem()

prob.model.add_subsystem("h2_production", HydrogenProduction(modeling_options=modeling_options), promotes=["*"])

prob.run_model()

wt_opt.model.list_outputs(units=True, print_arrays=True)
