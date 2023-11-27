from ROCv3 import ROCv3
from GBT_SCA import GBT_SCA
from Transactor import Transactor
from SlowControl_Interface import SlowControl_Interface
from utils import bytelen, load_yaml
from time import sleep
from gbtsca_constants import CTRL, GPIO, I2C
from utils import from_8bit_to_32bit



# Instantiate the Interface that connects to the hardware.
sc_interface = SlowControl_Interface()

# Instantiate the Transactor(s).
transactor = Transactor(sc_interface=sc_interface)

# Instantiate the GBT_SCA(s).
gbt_sca = GBT_SCA(transactor=transactor)


input('press enter')
print("==========================read device ID===========================")
gbt_sca._readDeviceID()

print("==========================read device ID===========================")


input('press enter')

#pin = gbt_sca.pin[0]
#i2c = gbt_sca.i2c[0]
#i2c = gbt_sca.i2c[0]
#i2c.set_speed(1000)

#i2c = []
#for i in range(16):
#    i2c.append(gbt_sca.i2c[i])
#    i2c[i].set_speed(1000)

#i2c._read_control_register()
#i2c._read_status_register()


#print('cache CRD', bin(transactor.cache_CRD))
#gbt_sca.i2c._read_enable_i2c()
#adc = gbt_sca.adc[0]
#adc.read()

gbt_sca.i2c._read_enable_i2c()

adc = []
for i in range(32):
    adc.append(gbt_sca.adc[i])

#print('cache CRD', bin(transactor.cache_CRD))
#gbt_sca.i2c._read_enable_i2c()
#dac = gbt_sca.dac[0]
#print('cache CRD', bin(transactor.cache_CRD))
#gbt_sca.i2c._read_enable_i2c()
#print('cache CRD', bin(transactor.cache_CRD))
#input('press enter')

input('press enter')

#print("========================After enable adc and dac===========================")
#print("==========================read device ID===========================")
#gbt_sca._readDeviceID()

#print("==========================read device ID===========================")


#input('press enter')


pin = []
for i in range(32):
    pin.append(gbt_sca.pin[i])

pin[0].set_mode('in')
pin[1].set_mode('in')
pin[2].set_mode('out')
pin[3].set_mode('out')
pin[4].set_mode('out')
pin[5].set_mode('in')
pin[6].set_mode('in')
pin[7].set_mode('out')
pin[8].set_mode('out')
pin[9].set_mode('out')
pin[10].set_mode('out')
pin[11].set_mode('out')
pin[12].set_mode('out')
pin[13].set_mode('out')
pin[14].set_mode('out')
pin[15].set_mode('out')
pin[16].set_mode('out')
pin[17].set_mode('out')
pin[18].set_mode('out')
pin[19].set_mode('out')
pin[20].set_mode('out')
pin[21].set_mode('out')
pin[22].set_mode('out')
pin[23].set_mode('out')
pin[24].set_mode('out')
pin[25].set_mode('out')
pin[26].set_mode('out')
pin[27].set_mode('out')
pin[28].set_mode('in')
pin[29].set_mode('in')
pin[30].set_mode('out')
pin[31].set_mode('out')

#switch on the LDOs to power the HGCROC.
pin[22].write(1)
pin[23].write(1)

# Need to wait some time for the LDO to power on
sleep(1)

# Set the SOFT_RSTB and I2C_RSTB to 1, which means "no reset"
pin[2].write(1)
pin[3].write(1)

# Set the HARD_RSTB to "1", "0", "1" to reset the whole HGCROC. (Has to do this upon power on)
pin[4].write(1)
pin[4].write(0)
pin[4].write(1)

pin[7].write(1)


#pin[20].write(1)
#pin[21].write(0)

pin[8].write(0)
pin[9].write(0)
pin[10].write(0)
pin[11].write(0)
pin[12].write(0)
pin[13].write(0)
pin[14].write(0)
pin[15].write(0)

sleep(2)

sleep(2)




#print(" ")
#print(" GPIOs")


#input('press enter')
#print("===================After setting the GPIO pins=====================")
#print("==========================read device ID===========================")
#gbt_sca._readDeviceID()

#print("==========================read device ID===========================")


gbt_sca.i2c._read_enable_i2c()

input('press enter')

for i in range(32):
    adc[i].read()

gbt_sca.i2c._read_enable_i2c()



#SCA_IOS = 819200255
'''
print("ERROR ROC1 (no error = 1): ", hex(SCA_IOS & 0x00000001))
print("PLL_LCK ROC1 (no error = 1): ", hex((SCA_IOS & 0x00000002)>>1))
print("ERROR ROC2 (no error = 1): ", hex((SCA_IOS & 0x00000020)>>5))
print("PLL_LCK ROC2 (no error = 1): ", hex((SCA_IOS & 0x00000040)>>6))
print("RSTB (no reset = 1): ", hex((SCA_IOS & 0x00000004)>>2))
print("I2C_RSTB (no reset = 1): ", hex((SCA_IOS & 0x00000008)>>3))
print("RESYNCLOAD (usually at 0): ", hex((SCA_IOS & 0x00000010)>>4))
print("SEL_CK_EXT (not used in ROCv3): ", hex((SCA_IOS & 0x00000040)>>6))
print("LED_ON_OFF (1: ON): ", hex((SCA_IOS & 0x00000080)>>7))
print("LED_DISABLE1 (1: OFF): ", hex((SCA_IOS & 0x00000100)>>8))
print("LED_DISABLE2 (1: OFF): ", hex((SCA_IOS & 0x00000200)>>9))
print("LED_DISABLE3 (1: OFF): ", hex((SCA_IOS & 0x00000400)>>10))
print("LED_DISABLE4 (1: OFF): ", hex((SCA_IOS & 0x00000800)>>11))
print("LED_DISABLE5 (1: OFF): ", hex((SCA_IOS & 0x00001000)>>12))
print("LED_DISABLE6 (1: OFF): ", hex((SCA_IOS & 0x00002000)>>13))
print("LED_DISABLE7 (1: OFF): ", hex((SCA_IOS & 0x00004000)>>14))
print("LED_DISABLE8 (1: OFF): ", hex((SCA_IOS & 0x00008000)>>15))
print("EN_HV0 (ALDOV1 BV1 (1: ON): ", hex((SCA_IOS & 0x00100000)>>20))
print("EN_HV1 (ALDOV1 BV2 (1: ON): ", hex((SCA_IOS & 0x00200000)>>21))
print("EN_HV2 (ALDOV2 BV1 (1: ON): ", hex((SCA_IOS & 0x00040000)>>18))
pirint("EN_HV3 (ALDOV2 BV2 (1: ON): ", hex((SCA_IOS & 0x00080000)>>19))
print("EN_LDO VDDA and VDDD (1: ON): ", hex((SCA_IOS & 0x00400000)>>22))
print("EN_SOFTSTART VDDA and VDDD (1: ON): ", hex((SCA_IOS & 0x00800000)>>23))
'''

#pin[4].write(0)
#pin[4].write(1)
#pin[3].write(0)
#pin[3].write(1)
#pin[2].write(0)
#pin[2].write(1)

#gbt_sca.i2c._read_enable_i2c()
#input('press enter')

#gbt_sca.pin._read_enable_gpio()

#gbt_sca.pin._get_mode()
#gbt_sca.pin._get_output()
#gbt_sca.pin._read()

#sleep(0.1)
#input('press enter')


#i2c = gbt_sca.i2c[0]

#input('press enter')
#address = 0x28
#data = 47
#address = int('{:08b}'.format(address)[::-1], 2)
#data = int('{:08b}'.format(data)[::-1], 2)


#i2c.write_test(address, data)
#i2c.write_10_test(address, data)

#for address in range(256):
#    transactor.sca_address = address
#    i2c.write_test(0x28, 47)

#i2c._read_control_register()
#i2c._read_status_register()

#print('control', bin(sc_interface.device.getNode("Transactor-Slow-Control-0_config.SCA_Status0").read()))
#print('status', bin(sc_interface.device.getNode("Transactor-Slow-Control-0_config.IC_Control0").read()))
#print('number of transactions', bin(sc_interface.device.getNode("Transactor-Slow-Control-0_config.SCA_Status0.NbrTransactions").read()))
#input('press enter')
#i2c._read_status_register()
#i2c.write_test(address, 47)
#i2c._read_status_register()
#i2c.set_speed(1000)
#print('control', bin(sc_interface.device.getNode("Transactor-Slow-Control-0_config.SCA_Status0").read()))
#print('status', bin(sc_interface.device.getNode("Transactor-Slow-Control-0_config.IC_Control0").read()))
#print('number of transactions', bin(sc_interface.device.getNode("Transactor-Slow-Control-0_config.SCA_Status0.NbrTransactions").read()))



#i2c._read_control_register()
#i2c._read_status_register()



'''
print("=============Write whatever to the HGCROC================")
print("==================Writing 47 to 0x28===================")
i2c.write_test(address, 47)
input('press enter')
print("==================Writing 11 to 0x29===================")
i2c.write_test(address + 1, 11)
input('press enter')
print("==================Writing 8 to 0x2a===================")
i2c.write_test(address + 2, 8)
input('press enter')


print("=============Read from the HGCROC================")
print("==================Writing 47 to 0x28===================")
i2c.write_test(address, 47)
input('press enter')
print("==================Writing 11 to 0x29===================")
i2c.write_test(address + 1, 11)
input('press enter')
print("==================Reading from 0x2a===================")
i2c.read_test(address + 2)
'''


# Instantiate the I2C(s).
#i2c = gbt_sca.i2c[0]
#i2c.set_speed(1000)
#input('press enter')
#i2c.read_test(0x28)
#address = int('{:08b}'.format(address)[::-1], 2)
#i2c.write_test(address, 47)
#input('press enter')
#address = 0x28
#data = 47
#address = int('{:08b}'.format(address)[::-1], 2)
#i2c.write_test(address, 47)
#input('press enter')
#i2c.read_test(address)

#for i in range(64):
#    transactor.reply_address = i
#    i2c.write_test(address, data)
#    i2c.set_speed(1000)
#for i in range(10, 256):
#    transactor.sca_address = i
#    i2c.write_test(address, data)
#    i2c.set_speed(1000)

#transactor.sca_address = 194
#i2c.write_test(address, data)

#
#i2c.write_test(address + 1, 11)
#input('press enter')
#i2c.write_test(address + 2, 8)

#input('press enter')
#i2c.read_test(address)
#input('press enter')
#i2c.read_test(address + 1)

#i2c.write_test(address, 47)
#input('press enter')
#i2c.write_test(address + 1, 11)
#input('press enter')
#i2c.read_test(address + 2)

#i2c.read_test(0x0)

#input('press enter')
#i2c._read_status_register()




#gbt_sca.pin._get_gpio_mode()
#gbt_sca.i2c._read_enable_i2c()
#input('press enter')

#i2c = []
#for i in range(16):
#    i2c.append(gbt_sca.i2c[i])
#    input('press enter')
#gbt_sca.pin._read_enable_gpio()
#input('press enter')

#i2c._read_status_register()
#i2c._read_enable_i2c()

#i2c.set_speed(1000)
#i2c.read_speed()


#i2c.set_speed(1000)
#i2c.read_speed()
#for address in range(128):
#    i2c.read_test(address)
#    i2c._read_status_register()

#i2c._read_status_register()
#i2c._read_enable_i2c()

#i2c.write_test(0x28, 47)
#for i in range(16):
#    for address in range(128):
#        i2c[i].write_test(address, 47)
#        i2c[i].read_test(address)
#        input('press enter')

#i2c = []
#for i in range(16):
#    i2c.append(gbt_sca.i2c[i])
#    i2c[i].set_speed(1000)
#    i2c[i].read_test(0x28)


#input('press enter')

#i2c.set_speed(1000)
#i2c.read_speed()
#gbt_sca.pin._get_gpio_mode()
#gbt_sca.pin._get_gpio_output()


#index = 0
#channel = I2C["CHANNEL_MAP"][index]

#transactor.write(channel, I2C["W_CTRL_REG"], data=0b00010011 << 24, comment='write I2C Ctrl register')
#transactor.send()

#i2c.write_test(0x36, 47)
#i2c.write_test(0x37, 11)
#i2c.write_test(0x38, 10)


#i2c._read_status_register()
#i2c._read_control_register()
#input('press enter')

#address = 0x28 << 24
#data = 47 << 16
#data += address
#transactor.write(
#    channel, I2C["W_7B_SINGLE"], data=0, comment=f'i2c {hex(channel)} single byte write to address {hex(address)}')
#transactor.send()

#input('press enter')
#i2c.write(0x28, 47)

#i2c.write_test(0x28, 47)
#i2c.read_test(0x28)
#i2c._read_status_register()
#i2c._read_control_register()
#input('press enter')

#i2c.write_test(0x28, 47)
#input('press enter')
#i2c._read_control_register()
#i2c._read_status_register()

#i2c.write_test(0x28 + 1, 11)
#i2c.write_test(0x28 + 2, 10)
#i2c.read_test(0x28 + 2)
#i2c.read_test(0x28)


#for i in range(128):
#    i2c.write_test(i, 47)

#i2c.write_test(0x28, 47)
#i2c.write_test(0x28 + 1, 11)
#i2c.write_test(0x28 + 2, 10)
#i2c.read_test(0x28)
#i2c.read_speed()

#pin[0].read_enable_gpio()


#i2c = []
#for i in range(16):
#    i2c.append(gbt_sca.i2c[i])
#    i2c[i].set_speed(1000)
#    i2c[i].write_test(0x28, 47)
#    i2c[i].read_test(0x0)
#    i2c[i]._read_status_register()
#    sleep(0.01)

#i2c[0]._read_enable_i2c()
#transactor.send()

#address = 0x28
#i2c.write(address=address, data=47)
#i2c.write(address=address + 1, data=11)
#i2c.write(address=address + 2, data=8)
#i2c.read(address=address + 2)


#roc = ROCv3(transport=i2c,
#      base_address=0x28,
#      name='roc',
#      reset_pin=0,
#      path_to_file='HGCROC3_I2C_params_regmap.csv')

#configuration = load_yaml('roc_test_config.yml')
#roc.configure(configuration)

#i2c.read(address=0x28 + 2)


##roc.read(configuration, from_hardware=True)

#i2c.set_speed(100)
#message = 0x1111222233
#i2c.write(0, message)
#transactor.send()
#i2c._read_control_register()
#transactor.send()

#i2c.set_speed(200)
#message = 0x111122
#i2c.write(0, message)
#transactor.send()
#i2c._read_control_register()
#transactor.send()

#i2c.set_speed(400)
#message = 0x11112222333344445555
#i2c.write(0x28, message)
#transactor.send()
#i2c._read_control_register()
#transactor.send()
#i2c.read(0, nbytes=10)
#transactor.send()

#i2c.set_speed(1000)
#message = 0x111122223333444455556666777788
#i2c.write(0, message)
#transactor.send()
#i2c._read_control_register()
#transactor.send()
#i2c.read(0, nbytes=15)
#transactor.send()

#for address in range(1024):
#    i2c.scan(address)
#    transactor.send()


#i2c = []
#for i in range(16):
#    i2c.append(gbt_sca.i2c[i])
#    for address in range(128):
#        i2c[i].scan(address)
#        transactor.send()



