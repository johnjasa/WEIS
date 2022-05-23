import numpy as np
import openmdao.api as om

try:
    from ROSCO_toolbox.ofTools.fast_io.output_processing import output_processing
    import ROSCO_toolbox
except:
    raise Exception(
        "Trying to read in an OpenFAST .outb file but ROSCO_toolbox is not installed. Please install ROSCO_toolbox to use its file processor."
    )


class ReadInPower(om.ExplicitComponent):
    def initialize(self):
        self.options.declare("filename")

    def setup(self):
        fast_out = output_processing()
        fast_data = fast_out.load_fast_out(self.options["filename"], verbose=False)[0]
        self.time = fast_data["Time"]
        self.wind = fast_data["Wind1VelX"]
        self.power = fast_data["GenPwr"]
        self.n_timesteps = len(self.power)

        self.add_output("time", shape=self.n_timesteps, units="s")
        self.add_output("wind", shape=self.n_timesteps, units="m/s")
        self.add_output("power", shape=self.n_timesteps, units="W")

    def compute(self, inputs, outputs):
        outputs["time"] = self.time
        outputs["wind"] = self.wind
        outputs["power"] = self.power
