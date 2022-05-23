import numpy as np
import openmdao.api as om

np.random.seed(314)


class SimpleWindModel(om.ExplicitComponent):
    def initialize(self):
        self.options.declare("n_timesteps", default=100)

    def setup(self):
        n_timesteps = self.options["n_timesteps"]
        self.add_input("time", shape=n_timesteps, units="h")
        self.add_output("wind", shape=n_timesteps, units="m/s")

    def compute(self, inputs, outputs):
        n_timesteps = self.options["n_timesteps"]
        outputs["wind"] = np.linspace(3.0, 15.0, n_timesteps)
