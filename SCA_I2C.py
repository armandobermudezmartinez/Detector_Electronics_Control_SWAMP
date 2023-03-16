class SCA_I2C:
    def __init__(self, gbt_sca=0, number_of_masters=0):
        if number_of_masters > 16:
            raise Exception("Number of I2C masters exceeds GBT_SCA I2C block")
        self.gbt_sca = gbt_sca
        self.number_of_masters = number_of_masters
        self._number_of_used_masters = 0

    def _enable(self, index, bus_frequency):
        self.gbt_sca.enable_i2c(index, bus_frequency)

    def _write(self, address, value):
        pass

    def _read(self, address, from_hardware):
        pass


class I2C:
    def __init__(self, sca_i2c, index=0, bus_frequency=100):
        sca_i2c._number_of_used_masters += 1
        if sca_i2c._number_of_used_masters > sca_i2c.number_of_masters:
            raise Exception("Number of I2C masters exceeds available ones")
        self.sca_i2c = sca_i2c
        self.index = index
        self.bus_frequency = bus_frequency
        self.sca_i2c._enable(self.index, self.bus_frequency)

    def write(self, bus, address, value):
        pass

    def read(self, bus, address, from_hardware):
        pass
