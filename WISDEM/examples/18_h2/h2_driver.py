import os

import numpy as np
import matplotlib.pyplot as plt

from wisdem.glue_code.runWISDEM import run_wisdem

## File management
run_dir = os.path.dirname(os.path.realpath(__file__))
fname_wt_input = run_dir + os.sep + "3p4MW_turbine.yaml"
fname_modeling_options = run_dir + os.sep + "modeling_options.yaml"
fname_analysis_options = run_dir + os.sep + "analysis_options.yaml"

wt_opt, modeling_options, opt_options = run_wisdem(fname_wt_input, fname_modeling_options, fname_analysis_options)

wt_opt.model.list_outputs(includes=["*h2*"], units=True, print_arrays=True)


wind = wt_opt.get_val("h2.simple_wind.wind", units="m/s")
power = wt_opt.get_val("h2.compute_power.p_wind", units="MW")
h2_prod_rate = wt_opt.get_val("h2.simple_electrolyzer.h2_prod_rate", units="kg/h")

fig, axarr = plt.subplots(3, 1)

axarr[0].plot(wind, power)
axarr[0].set_ylabel("Power, MW")

axarr[1].plot(wind, h2_prod_rate)
axarr[1].set_ylabel("H2 production rate, kg/h")

axarr[2].plot(wind, h2_prod_rate / power)
axarr[2].set_ylabel("H2 production rate / power")
axarr[2].set_xlabel("Wind speed, m/s")

plt.savefig("fill_electrolyzer_stacks_first.png")
