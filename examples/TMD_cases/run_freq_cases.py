import numpy as np
from weis.glue_code.runWEIS     import run_weis
import os, time, sys
from wisdem.inputs import load_yaml, write_yaml

## File management
run_dir                = os.path.dirname( os.path.realpath(__file__) ) + os.sep
fname_wt_input         = os.path.realpath(os.path.join(run_dir,"IEA-15-floating_wTMDs_tower.yaml"))
fname_modeling_options = run_dir + "modeling_options_tower.yaml"
fname_analysis_options = run_dir + "analysis_options_tower_DVs_no_opt.yaml"


data = np.loadtxt('results.txt', delimiter=',')

mass = data[:, 0]
diameters = data[:, 1:4]
thickness = data[:, 4:7]
tower_damage = data[:, 7]
freqs = data[:, 8]

indices = np.argsort(freqs)

freq_lower_bound = 0.36
freq_upper_bound = 0.39

for idx in indices:
    freq = freqs[idx]
    diameter = list(diameters[idx])
    thick = list(thickness[idx])
    if freq_lower_bound < freq < freq_upper_bound:
        print()
        print('freq', freq)
        print('diameter', diameter)
        print('thick', thick)
        
        geom = load_yaml(fname_wt_input)

        for jdx, val in enumerate(diameter):
            geom["components"]["tower"]["outer_shape_bem"]["outer_diameter"]["values"][jdx] = float(val)
        for jdx, val in enumerate(thick):
            geom["components"]["tower"]["internal_structure_2d_fem"]["layers"][0]["thickness"]["values"][jdx] = float(val)
        
        new_geom = f"{fname_wt_input.split('/')[-1].split('.')[0]}_{freq}.yaml"
        write_yaml(geom, new_geom)
        
        wt_opt, modeling_options, opt_options = run_weis(new_geom, fname_modeling_options, fname_analysis_options)
        
        print('Damage:', wt_opt['aeroelastic.damage_tower_base'])
exit()