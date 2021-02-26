import numpy as np
import os
import weis.control.LinearModel as lin_mod
import weis.aeroelasticse.LinearFAST as lin_fast

weis_dir                 = os.path.dirname( os.path.dirname (os.path.dirname(os.path.realpath(__file__)) ) )

# 0. Load linear models from gen_linear_model() in WEIS/wies/aeroelasticse/LinearFAST.py
lin_fast.gen_linear_model([16])

# 1. Set up linear turbine model by running mbc transformation
# Load system from OpenFAST .lin files
lin_file_dir = os.path.join(weis_dir,'outputs/iea_semi_lin')
linTurb = lin_mod.LinearTurbineModel(lin_file_dir,reduceStates=False)

A = np.squeeze(linTurb.A_ops)
B = np.squeeze(linTurb.B_ops)
C = np.squeeze(linTurb.C_ops)
D = np.squeeze(linTurb.D_ops)

print()
print('A\n', A)
print()
print('B\n', B)
print()
print('C\n', C)
print()
print('D\n', D)

