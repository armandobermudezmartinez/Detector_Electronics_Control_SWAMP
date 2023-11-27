from gbtsca_constants import CTRL, I2C
from utils import from_8bit_to_32bit, get_4bytes, bytelen


class SCA_I2C:
    def __init__(self, transactor):
        self.transactor = transactor
        self.number_of_i2cs = 16
        self.i2c = [None] * 16
        #self.cache_CRC = 0
        #self.cache_CRD = 0

    def __getitem__(self, index):
        if index not in range(self.number_of_i2cs):
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
        return speeds[speed]

    def _read_speed(self, index):
        channel = I2C["CHANNEL_MAP"][index]
        self.transactor.write(
            channel, I2C["R_CTRL_REG"], comment=f'Read communication speed of I2C {index}')



class I2C_Master(SCA_I2C):
    def __init__(self, transactor, index):
        super().__init__(transactor)
        self.index = index
        self.channel = I2C["CHANNEL_MAP"][self.index]
        self.ctrl_cache = 0x0
    
        #self.transactor.send()

        #self.speed = 100
        #self.set_speed(self.speed)
 
    def set_speed(self, new_speed):
        speed = self._set_speed(self.index, new_speed)
        self.ctrl_cache =  (self.ctrl_cache & ~I2C["MASK_CTRL_REG_SPEED"]) | speed
        self.speed = new_speed
        self.transactor.send()

    def read_speed(self):
        self._read_speed(self.index)
        self.transactor.send()

    def write(self, address, data):
        self.transactor.write(
            self.channel, I2C["R_CTRL_REG"], comment=f'Read ctrlBits i2c {self.index}')
        ctrlBits = self.ctrl_cache
        nbytes = bytelen(data)
        d3 = (ctrlBits & ~I2C["MASK_CTRL_REG_NBYTE"]) | (nbytes << 2)
        self.transactor.write(self.channel, I2C["W_CTRL_REG"], data=from_8bit_to_32bit(
            d3), comment='write I2C Ctrl register')
        self.ctrl_cache = d3

        self.transactor.send()
        self._read_status_register()        

        self.transactor.write(
            self.channel, I2C["W_DATA_0"], data=get_4bytes(data, 0), comment='write to sca i2c register W_Data 0')
        if nbytes > 4:
            self.transactor.write(
                self.channel, I2C["W_DATA_1"], data=get_4bytes(data, 1), comment='write to sca i2c register W_Data 1')
        if nbytes > 8:
            self.transactor.write(
                self.channel, I2C["W_DATA_2"], data=get_4bytes(data, 2), comment='write to sca i2c register W_Data 2')
        if nbytes > 12:
            self.transactor.write(
                self.channel, I2C["W_DATA_3"], data=get_4bytes(data, 3), comment='write to sca i2c register W_Data 3')

        self.transactor.send()
        self._read_status_register()

        self._send_address(address)
        self._read_status_register()

    def read(self, address, nbytes=16):
        self.transactor.write(
            self.channel, I2C["R_CTRL_REG"], comment=f'Read ctrlBits i2c {self.index}')
        ctrlBits = self.ctrl_cache
        d3 = (ctrlBits & ~I2C["MASK_CTRL_REG_NBYTE"]) | (nbytes << 2)
        self.transactor.write(self.channel, I2C["W_CTRL_REG"], data=from_8bit_to_32bit(
            d3), comment='write I2C Ctrl register')
        self.ctrl_cache = d3

        self.transactor.send()

        self._send_address(address=address)

        self.transactor.write(
            self.channel, I2C["R_DATA_0"], comment='read from sca i2c register R_Data 0')
        if nbytes > 4:
            self.transactor.write(
                self.channel, I2C["R_DATA_1"], comment='read from sca i2c register R_Data 1')
        if nbytes > 8:
            self.transactor.write(
                self.channel, I2C["R_DATA_2"], comment='read from sca i2c register R_Data 2')
        if nbytes > 12:
            self.transactor.write(
                self.channel, I2C["R_DATA_3"], comment='read from sca i2c register R_Data 3')

        self.transactor.send()

    def _send_address(self, address):
        self.transactor.write(
            self.channel, I2C["W_7B_MULTI"], data=address, comment='send i2c address', pop_id=0)
        print(hex(address))
        address = address << 24
        print(hex(address))
        self.transactor.send()

    def _read_control_register(self):
        self.transactor.write(
            self.channel, I2C["R_CTRL_REG"], comment=f'Read ctrlBits i2c {self.index}')
        self.transactor.send()

    def _read_status_register(self):
        self.transactor.write(
            self.channel, I2C["R_STATUS_REG"], comment=f'Read i2c status register')
        self.transactor.send()

    #def _scan(self, address):
    #    self.transactor.write(
    #        self.channel, I2C["W_7B_MULTI"], data=from_8bit_to_32bit(address), comment=f'Checking address {address} (bx{bin(address)}) of I2C {self.index}', pop_id=0)
    #    self.transactor.send()

    def read_test(self, address):
        address = address << 24
        self.transactor.write(
            self.channel, I2C["R_7B_SINGLE"], data=address, comment=f'i2c {self.index} single byte read address {hex(address)}', pop_id=0)

        self.transactor.send()

    def write_test(self, address, data):
        d = data
        address = address << 24
        data = data << 16
        #print(bin(address))
        #print(bin(data))
        #print(bin(data | address))
        #address = address << 16
        #data = data << 24
        data |= address        
        self.transactor.write(
            self.channel, I2C["W_7B_SINGLE"], data=data, comment=f'i2c {self.index} single byte write {d} to address {hex(address)}', pop_id=0)

        self.transactor.send()

    def write_10_test(self, address, data):
        address = (address << 16)
        address |= (0b111000 << 24)
        #print('address', bin(address))
        data = (data << 8)
        data |= address
        #print('address + data', bin(data))
        self.transactor.write(
            self.channel, I2C["W_10B_SINGLE"], data=data, comment=f'i2c {self.index} 10 bits address write to address {hex(address)}')

        self.transactor.send()

