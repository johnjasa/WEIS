import numpy as np
import openmdao.api as om

try:
    from weis.aeroelasticse.turbsim_file import TurbSimFile
except:
    raise Exception(
        "Trying to read in a TurbSim file but WEIS is not installed. Please install WEIS to use its file processor."
    )


class ReadInWind(om.ExplicitComponent):
    def initialize(self):
        self.options.declare("filename")

        out = TurbSimFile(self.options["filename"])
        iy, iz = out._iMid()
        self.wind = out["u"][0, :, iy, iz]
        self.time = out["t"]
        self.n_timesteps = len(self.time)

    def setup(self):
        self.add_output("time", shape=self.n_timesteps, units="s")
        self.add_output("wind", shape=self.n_timesteps, units="m/s")

    def compute(self, inputs, outputs):
        outputs["time"] = self.time
        outputs["wind"] = self.wind
