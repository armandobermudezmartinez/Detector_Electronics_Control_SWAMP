from gbtsca_constants import CTRL, I2C
from utils import from_8bit_to_32bit


class SCA_I2C:
    def __init__(self, transactor):
        self.transactor = transactor
        self.i2c = [None] * 16

    def __getitem__(self, index):
        if index not in range(16):
            raise Exception(
                "I2C-channel index out of permissible range [0, 15]")
        if self.i2c[index] is None:
            self._enable_i2c(index)
            self.i2c[index] = I2C_Master(self.transactor, index)
        return self.i2c[index]

    def _enable_i2c(self, index):
        index_bit = (1 << index)

        INPUTMASK_CRB = 0x001f
        INPUTMASK_CRC = 0x1fe0
        INPUTMASK_CRD = 0xe000

        if (index_bit & INPUTMASK_CRB):
            d3 = 0
            if ((1 << 0) & index_bit):
                d3 = d3 | CTRL["MASK_CRB_I2C0"]
            if ((1 << 1) & index_bit):
                d3 = d3 | CTRL["MASK_CRB_I2C1"]
            if ((1 << 2) & index_bit):
                d3 = d3 | CTRL["MASK_CRB_I2C2"]
            if ((1 << 3) & index_bit):
                d3 = d3 | CTRL["MASK_CRB_I2C3"]
            if ((1 << 4) & index_bit):
                d3 = d3 | CTRL["MASK_CRB_I2C4"]

            m3 = CTRL["MASK_CRB_I2C0"] | CTRL["MASK_CRB_I2C1"] | CTRL[
                "MASK_CRB_I2C2"] | CTRL["MASK_CRB_I2C3"] | CTRL["MASK_CRB_I2C4"]
            mask = from_8bit_to_32bit(m3)
            data = from_8bit_to_32bit(d3)
            self.transactor.write(CTRL["CHANNEL_CTRL"],
                                  CTRL["W_CRB"], mask=mask, data=data, comment=f'Enable I2C master {index}')

        if (index_bit & INPUTMASK_CRC):
            d3 = 0
            if ((1 << 5) & index_bit):
                d3 = d3 | CTRL["MASK_CRC_I2C5"]
            if ((1 << 6) & index_bit):
                d3 = d3 | CTRL["MASK_CRC_I2C6"]
            if ((1 << 7) & index_bit):
                d3 = d3 | CTRL["MASK_CRC_I2C7"]
            if ((1 << 8) & index_bit):
                d3 = d3 | CTRL["MASK_CRC_I2C8"]
            if ((1 << 9) & index_bit):
                d3 = d3 | CTRL["MASK_CRC_I2C9"]
            if ((1 << 10) & index_bit):
                d3 = d3 | CTRL["MASK_CRC_I2C10"]
            if ((1 << 11) & index_bit):
                d3 = d3 | CTRL["MASK_CRC_I2C11"]
            if ((1 << 12) & index_bit):
                d3 = d3 | CTRL["MASK_CRC_I2C12"]

            m3 = CTRL["MASK_CRC_I2C5"] | CTRL["MASK_CRC_I2C6"] | CTRL["MASK_CRC_I2C7"] | CTRL[
                "MASK_CRC_I2C8"] | CTRL["MASK_CRC_I2C9"] | CTRL["MASK_CRC_I2C10"] | CTRL[
                "MASK_CRC_I2C11"] | CTRL["MASK_CRC_I2C12"]

            mask = from_8bit_to_32bit(m3)
            data = from_8bit_to_32bit(d3)
            self.transactor.write(CTRL["CHANNEL_CTRL"],
                                  CTRL["W_CRC"], mask=mask, data=data, comment=f'Enable I2C master {index}')

        if (index_bit & INPUTMASK_CRD):
            d3 = 0
            if ((1 << 13) & index_bit):
                d3 = d3 | CTRL["MASK_CRD_I2C13"]
            if ((1 << 14) & index_bit):
                d3 = d3 | CTRL["MASK_CRD_I2C14"]
            if ((1 << 15) & index_bit):
                d3 = d3 | CTRL["MASK_CRD_I2C15"]

            m3 = CTRL["MASK_CRD_I2C13"] | CTRL[
                "MASK_CRD_I2C14"] | CTRL["MASK_CRD_I2C15"]

            mask = from_8bit_to_32bit(m3)
            data = from_8bit_to_32bit(d3)
            self.transactor.write(CTRL["CHANNEL_CTRL"],
                                  CTRL["W_CRD"], mask=mask, data=data, comment=f'Enable I2C master {index}')

    def _read_enable_i2c(self):
        self.transactor.write(
            CTRL["CHANNEL_CTRL"], CTRL["R_CRB"], comment='Read which I2C masters are enabled (register B)')

        self.transactor.write(
            CTRL["CHANNEL_CTRL"], CTRL["R_CRC"], comment='Read which I2C masters are enabled (register C)')

        self.transactor.write(
            CTRL["CHANNEL_CTRL"], CTRL["R_CRD"], comment='Read which I2C masters are enabled (register D)')

    def _set_speed(self, index, speed):
        channel = I2C["CHANNEL_MAP"][index]
        if speed not in [100, 200, 400, 1000]:
            raise Exception(
                "Bus speed not among permissible values 100, 200, 400, 1000 kHz")
        speeds = {
            100: 0b00,
            200: 0b01,
            400: 0b10,
            1000: 0b11
        }

        m3, d3 = I2C["MASK_CTRL_REG_SPEED"], speeds[speed]
        mask, data = from_8bit_to_32bit(m3), from_8bit_to_32bit(d3)
        self.transactor.write(
            channel, I2C["W_CTRL_REG"], mask=mask, data=data, comment=f'Set communication speed of I2C {index} to {speed} kHz')

    def _read_speed(self, index):
        channel = I2C["CHANNEL_MAP"][index]
        self.transactor.write(
            channel, I2C["R_CTRL_REG"], comment=f'Read communication speed of I2C {index}')

    def read(self):
        pass

    def scanner(self):
        pass


class I2C_Master(SCA_I2C):
    def __init__(self, transactor, index):
        super().__init__(transactor)
        self.index = index
        self.speed = 100
        self.set_speed(self.speed)

    def set_speed(self, new_speed):
        self._set_speed(self.index, new_speed)
        self.speed = new_speed

    def read_speed(self):
        self._read_i2c_speed(self.index)

    def write(self, bus, address, value):
        pass

    def read(self, bus, address, from_hardware):
        pass
