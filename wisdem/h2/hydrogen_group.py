import openmdao.api as om

from wisdem.h2.simple_wind import SimpleWindModel
from wisdem.h2.electrolyzer import SimpleElectrolyzerModel
from wisdem.h2.read_in_wind import ReadInWind
from wisdem.h2.compute_power import ComputePower
from wisdem.h2.read_in_power import ReadInPower


class HydrogenProduction(om.Group):
    """"""

    def initialize(self):
        self.options.declare("modeling_options")

    def setup(self):
        modeling_options = self.options["modeling_options"]
        n_timesteps = modeling_options["WISDEM"]["HydrogenProduction"]["n_timesteps"]
        read_in_wind_file = modeling_options["WISDEM"]["HydrogenProduction"]["read_in_wind_file"]
        read_in_power_signal = modeling_options["WISDEM"]["HydrogenProduction"]["read_in_power_signal"]

        if read_in_power_signal:
            self.add_subsystem(
                "read_in_power",
                ReadInPower(filename=modeling_options["WISDEM"]["HydrogenProduction"]["power_filename"]),
                promotes=["*"],
            )
        else:
            if read_in_wind_file:
                self.add_subsystem(
                    "read_in_wind",
                    ReadInWind(filename=modeling_options["WISDEM"]["HydrogenProduction"]["wind_filename"]),
                    promotes=["*"],
                )
            else:
                # Use a dummy wind profile
                self.add_subsystem("simple_wind", SimpleWindModel(n_timesteps=n_timesteps), promotes=["*"])

            self.add_subsystem("compute_power", ComputePower(modeling_options=modeling_options), promotes=["*"])

        self.add_subsystem("simple_electrolyzer", SimpleElectrolyzerModel(n_timesteps=n_timesteps), promotes=["*"])
