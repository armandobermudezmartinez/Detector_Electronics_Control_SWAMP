from gbtsca_constants import CTRL, I2C
from utils import from_8bit_to_32bit, get_4bytes, bytelen, get_byte


class SCA_I2C:
    def __init__(self, transactor):
        self.transactor = transactor
        self.number_of_i2cs = 16
        self.i2c = [None] * 16
        self.ctrl_cache = 0x0

    def __getitem__(self, index):
        if index not in range(self.number_of_i2cs):
            raise Exception(
                "I2C-channel index out of permissible range [0, 15]")
        if self.i2c[index] is None:
            self._enable(index)
            self.i2c[index] = I2C_Master(self, index)
        return self.i2c[index]

    def _enable(self, index):
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
            cache = from_8bit_to_32bit(self.transactor.cache_CRB)
            self.transactor.write(CTRL["CHANNEL_CTRL"],
                                  CTRL["W_CRB"], mask=mask, data=data, cache=cache, comment=f'Enable I2C master {index}')
            self.transactor.cache_CRB |= d3

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
            cache = from_8bit_to_32bit(self.transactor.cache_CRC)
            self.transactor.write(CTRL["CHANNEL_CTRL"],
                                  CTRL["W_CRC"], mask=mask, data=data, cache=cache, comment=f'Enable I2C master {index}')
            self.transactor.cache_CRC |= d3

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
            cache = from_8bit_to_32bit(self.transactor.cache_CRD)
            self.transactor.write(CTRL["CHANNEL_CTRL"],
                                  CTRL["W_CRD"], mask=mask, data=data, cache=cache, comment=f'Enable I2C master {index}')
            self.transactor.cache_CRD |= d3

        self.transactor.send()

    def _read_enable_i2c(self):
        self.transactor.write(
            CTRL["CHANNEL_CTRL"], CTRL["R_CRB"], comment='Read which I2C masters are enabled (register B)')

        self.transactor.write(
            CTRL["CHANNEL_CTRL"], CTRL["R_CRC"], comment='Read which I2C masters are enabled (register C)')

        self.transactor.write(
            CTRL["CHANNEL_CTRL"], CTRL["R_CRD"], comment='Read which I2C masters are enabled (register D)')

        self.transactor.send()

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
        self.ctrl_cache =  (self.ctrl_cache & ~I2C["MASK_CTRL_REG_SPEED"]) | speeds[speed]

    def _read_speed(self, index):
        channel = I2C["CHANNEL_MAP"][index]
        self.transactor.write(
            channel, I2C["R_CTRL_REG"], comment=f'Read communication speed of I2C {index}')

    def _7bit_addressing_single_byte_write(self, index, address, data):
        channel = I2C["CHANNEL_MAP"][index]
        address = address << 24
        _data = data
        data = data << 16
        data |= address
        self.transactor.write(
            channel, I2C["W_7B_SINGLE"], data=data, comment=f'i2c {index}, 7-bit addressing mode write {_data} to address {hex(address)}')

    def _10bit_addressing_single_byte_write(self, index, address, data):
        channel = I2C["CHANNEL_MAP"][index]
        last_bits = 0b1110 << 26
        address = (address << 16)
        address |= last_bits
        _data = data
        data = (data << 8)
        data |= address
        self.transactor.write(
            channel, I2C["W_10B_SINGLE"], data=data, comment=f'i2c {index}, 10-bit addressing mode write to address {hex(address)}')

    def _7bit_addressing_multi_byte_write(self, index, address, data):
        channel = I2C["CHANNEL_MAP"][index]
        self.transactor.write(
            channel, I2C["R_CTRL_REG"], comment=f'Read ctrlBits i2c {index}')
        ctrlBits = self.ctrl_cache
        nbytes = bytelen(data)
        self.transactor.send()

        d3 = (ctrlBits & ~I2C["MASK_CTRL_REG_NBYTE"]) | (nbytes << 2)
        self.transactor.write(channel, I2C["W_CTRL_REG"], data=from_8bit_to_32bit(
            d3), comment='write I2C Ctrl register')
        self.ctrl_cache = d3

        self.transactor.send()

        self.transactor.write(
            channel, I2C["W_DATA_0"], data=get_4bytes(data, 0), comment='write to sca i2c register W_Data 0')
        if nbytes > 4:
            self.transactor.write(
                channel, I2C["W_DATA_1"], data=get_4bytes(data, 1), comment='write to sca i2c register W_Data 1')
        if nbytes > 8:
            self.transactor.write(
                channel, I2C["W_DATA_2"], data=get_4bytes(data, 2), comment='write to sca i2c register W_Data 2')
        if nbytes > 12:
            self.transactor.write(
                channel, I2C["W_DATA_3"], data=get_4bytes(data, 3), comment='write to sca i2c register W_Data 3')

        self.transactor.send()
        self._send_address(index, address)

    def _send_address(self, index, address):
        channel = I2C["CHANNEL_MAP"][index]
        address = address << 24
        self.transactor.write(
            channel, I2C["W_7B_MULTI"], data=address, comment=f'send address to i2c {index}', pop_id=0)
        address = address << 24
        self.transactor.send()


    def _7bit_addressing_single_byte_read(self, index, address):
        channel = I2C["CHANNEL_MAP"][index]
        address = address << 24
        self.transactor.write(
            channel, I2C["R_7B_SINGLE"], data=address, comment=f'i2c {index}, 7-bit addressing mode read from address {hex(address)}')

    def _10bit_addressing_single_byte_read(self, index, address):
        channel = I2C["CHANNEL_MAP"][index]
        last_bits = 0b1110 << 26
        address = (address << 16)
        address |= last_bits 
        self.transactor.write(
            channel, I2C["R_7B_SINGLE"], data=address, comment=f'i2c {index}, 10-bit addressing mode read from address {hex(address)}')


    def _7bit_addressing_multi_byte_read(self, index, address, number_of_bytes):
        channel = I2C["CHANNEL_MAP"][index]
        self.transactor.write(
            channel, I2C["R_CTRL_REG"], comment=f'Read ctrlBits i2c {index}')
        ctrlBits = self.ctrl_cache
        d3 = (ctrlBits & ~I2C["MASK_CTRL_REG_NBYTE"]) | (number_of_bytes << 2)
        self.transactor.write(channel, I2C["W_CTRL_REG"], data=from_8bit_to_32bit(
            d3), comment='write I2C Ctrl register')
        self.ctrl_cache = d3

        self.transactor.send()

        self._send_address(index=index, address=address)

        self.transactor.write(
            channel, I2C["R_DATA_0"], comment='read from sca i2c register R_Data 0')
        if number_of_bytes > 4:
            self.transactor.write(
                channel, I2C["R_DATA_1"], comment='read from sca i2c register R_Data 1')
        if number_of_bytes > 8:
            self.transactor.write(
                channel, I2C["R_DATA_2"], comment='read from sca i2c register R_Data 2')
        if number_of_bytes > 12:
            self.transactor.write(
                channel, I2C["R_DATA_3"], comment='read from sca i2c register R_Data 3')

        self.transactor.send()


class I2C_Master(SCA_I2C):
    def __init__(self, sca_i2c, index):
        self.index = index
        self.channel = I2C["CHANNEL_MAP"][self.index]
        self._speed = 100
        self.sca_i2c = sca_i2c

    def speed(self, new_speed):
        self.sca_i2c._set_speed(self.index, new_speed)
        self._speed = new_speed

        self.sca_i2c.transactor.send()

    def read_speed(self):
        self.sca_i2c._read_speed(self.index)
        self.sca_i2c.transactor.send()

    def write(self, address, data, communication_mode=0):
        if communication_mode == 0:
            self.sca_i2c._7bit_addressing_single_byte_write(self.index, address, data)
            self.sca_i2c.transactor.send()
        elif (communication_mode == 1):
            self.sca_i2c._10bit_addressing_single_byte_write(self.index, address, data)
            self.sca_i2c.transactor.send()
        elif (communication_mode == 2):
            self.sca_i2c._7bit_addressing_multi_byte_write(self.index, address, data)
        else:
            raise Exception("Allowed communication modes are 0: 7-bit addressing single-byte write, 1: 7-bit addressing single-byte write, 2: 7-bit addressing multi-byte write")

    def read(self, address, communication_mode=0, number_of_bytes=16):
        if communication_mode == 0:
            self.sca_i2c._7bit_addressing_single_byte_read(self.index, address)
            self.sca_i2c.transactor.send()
        elif (communication_mode == 1):
            self.sca_i2c._10bit_addressing_single_byte_read(self.index, address)
        elif (communication_mode == 2):
            self.sca_i2c._7bit_addressing_multi_byte_read(self.index, address, number_of_bytes)
        else:
            raise Exception("Allowed communication modes are 0: 7-bit addressing single-byte read, 1: 7-bit addressing single-byte read, 2: 7-bit addressing multi-byte read")
        #print("payload", self.sca_i2c.transactor.response[-1]["payload"], get_byte(self.sca_i2c.transactor.response[-1]["payload"], 2))
        return get_byte(self.sca_i2c.transactor.response[-1]["payload"], 2)

    def _read_control_register(self):
        self.sca_i2c.transactor.write(
            self.channel, I2C["R_CTRL_REG"], comment=f'Read ctrlBits i2c {self.index}')
        self.sca_i2c.transactor.send()

    def _read_status_register(self):
        self.sca_i2c.transactor.write(
            self.channel, I2C["R_STATUS_REG"], comment=f'Read i2c status register')
        self.sca_i2c.transactor.send()

