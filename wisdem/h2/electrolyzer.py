# Copyright 2022 NREL

# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.


import numpy as np
import openmdao.api as om
import matplotlib.pyplot as plt


class electrolyzer:
    def __init__(self):
        pass

    def converter_efficiency(self, Pdc):
        a = -7.798034801
        b = -20.201370915
        c = 8.704400555
        d = -17.680617589

        efficiency = (a * Pdc) / (b + Pdc) + (c * Pdc) / (d + Pdc)
        return efficiency

    def convert_ac_to_dc(self, Pac):
        a = 0.000056676
        b = 1.046711474
        c = 18.856165577
        Pdc_plus = (-b + np.sqrt(b ** 2 - 4 * a * (c - Pac))) / (2 * a)
        Pdc_minus = (-b - np.sqrt(b ** 2 - 4 * a * (c - Pac))) / (2 * a)

        return Pdc_minus, Pdc_plus

    def stack_current_from_voltage(self, V_in, T):
        a1 = -0.000146297
        b1 = 0.025443613
        c1 = -0.178823095
        d1 = 168.652142633

        I = (V_in - c1 * T - d1) / (a1 * T + b1)
        return I

    def stack_voltage_from_current(self, I_in, T):
        a1 = -0.000146297
        b1 = 0.025443613
        c1 = -0.178823095
        d1 = 168.652142633

        V = a1 * I_in * T + b1 * I_in + c1 * T + d1
        return V

    def stack_current_from_power(self, P_in, T):
        a = -0.001385949
        b = 0.085812325
        c = 0.007882033
        d = 5.101696939
        e = -6.423467186
        f = 148.372002335

        I = a * P_in ** 2 + b * T ** 2 + c * P_in * T + d * P_in + e * T + f
        return I

    def getH2GenRate(self, kw, eff=0.7):
        hhv = 39.4  # kWh/kg
        energy_req = hhv / eff
        mflow = kw / energy_req

        return mflow


class SimpleElectrolyzerModel(om.ExplicitComponent):
    def setup(self):
        n_timesteps = self.options["n_timesteps"]
        self.add_input("p_wind", shape_by_conn=True, units="kW")
        self.add_input("time", shape_by_conn=True, units="h")
        self.add_output("h2_prod_rate", shape_by_conn=True, copy_shape="time", units="kg/h")
        self.add_output("h2_produced", units="kg")

        self.n_electrolyzers = 5
        self.elec_stack_size = 750  # kW
        self.distribution_type = "even"  # even or full; (divided wind power
        # evenly across electrolyzers or run as many
        # at capacity as possible and the rest empty)

        self.elec = electrolyzer()

    def compute(self, inputs, outputs):
        if self.distribution_type == "even":
            # Split power evenly across all electrolyzer stacks
            Pdc_minus, Pdc_plus = self.elec.convert_ac_to_dc(inputs["p_wind"] / self.n_electrolyzers)
            h2_prod_rate = self.elec.getH2GenRate(Pdc_plus, eff=0.7) * self.n_electrolyzers
            outputs["h2_prod_rate"] = h2_prod_rate

        elif self.distribution_type == "full":
            p_wind = inputs["p_wind"]
            for idx, power in enumerate(p_wind):
                h2_prod_rate = 0.0

                num_stacks_at_full = power // self.elec_stack_size
                Pdc_minus, Pdc_plus = self.elec.convert_ac_to_dc(self.elec_stack_size)
                h2_prod_rate = self.elec.getH2GenRate(Pdc_plus, eff=0.7) * num_stacks_at_full

                leftover_power = power % self.elec_stack_size
                Pdc_minus, Pdc_plus = self.elec.convert_ac_to_dc(leftover_power)
                h2_prod_rate += self.elec.getH2GenRate(Pdc_plus, eff=0.7)

                outputs["h2_prod_rate"][idx] = h2_prod_rate

        outputs["h2_produced"] = np.trapz(outputs["h2_prod_rate"], inputs["time"])


if __name__ == "__main__":
    prob = om.Problem(model=om.Group())
    prob.model.add_subsystem("electrolyzer", SimpleElectrolyzerModel(), promotes=["*"])

    prob.setup()
    prob["p_wind"] = np.linspace(2000.0, 4000.0, 100)
    prob["time"] = np.linspace(0.0, 100.0, 100)

    prob.run_model()

    prob.model.list_outputs(print_arrays=True)
