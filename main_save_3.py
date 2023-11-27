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
sca = GBT_SCA(transactor=transactor)

#print("==========================read device ID===========================")
#sca._read_device_id()

#print("========================After enable adc and dac===========================")
#print("==========================read device ID===========================")
adc = sca.adc[0]
dac = sca.dac['a']

#sca._read_device_id()

#input('press enter')


pin = []
for i in range(32):
    pin.append(sca.pin[i])

pin[0].mode('in')
pin[1].mode('in')
pin[2].mode('out')
pin[3].mode('out')
pin[4].mode('out')
pin[5].mode('in')
pin[6].mode('in')
pin[7].mode('out')
pin[8].mode('out')
pin[9].mode('out')
pin[10].mode('out')
pin[11].mode('out')
pin[12].mode('out')
pin[13].mode('out')
pin[14].mode('out')
pin[15].mode('out')
pin[16].mode('out')
pin[17].mode('out')
pin[18].mode('out')
pin[19].mode('out')
pin[20].mode('out')
pin[21].mode('out')
pin[22].mode('out')
pin[23].mode('out')
pin[24].mode('out')
pin[25].mode('out')
pin[26].mode('out')
pin[27].mode('out')
pin[28].mode('in')
pin[29].mode('in')
pin[30].mode('out')
pin[31].mode('out')

#switch on the LDOs to power the HGCROC.
pin[22].write(1)
pin[23].write(1)

# Need to wait some time for the LDO to power on
sleep(1)

# Set the SOFT_RSTB and I2C_RSTB to 1, which means "no reset"
pin[2].write(1)
pin[3].write(1)

# Set the HARD_RSTB to "1", "0", "1" to reset the whole HGCROC. (Has to do this upon power on)
#################
pin[4].write(1)
pin[4].write(0)
pin[4].write(1)
#################
pin[7].write(1)
pin[8].write(0)
pin[9].write(0)
pin[10].write(0)
pin[11].write(0)
pin[12].write(0)
pin[13].write(0)
pin[14].write(0)
pin[15].write(0)

sleep(1)

#print(" ")
#print(" GPIOs")

input('press enter')
sca.pin._read()
input('press enter')

pin[2].write(1)
pin[2].write(0)
pin[2].write(1)

pin[3].write(1)
pin[3].write(0)
pin[3].write(1)

pin[4].write(1)
pin[4].write(0)
pin[4].write(1)

input('press enter')
sca.pin._read()

input('press enter')
#adc = []
#for i in range(32):
#    adc.append(gbt_sca.adc[i])
#    adc[i].read()

#adc = sca.adc[31]
#while True:
#    adc.read()
#    print(50 * "#", "The SCA Temperature is:", transactor.response[0]['payload'], 50 * "#")
#    sleep(1) 

#adc = []
#for i in range(32):
#    adc.append(sca.adc[i])
#    adc[i].read()

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

#sleep(0.1)
#input('press enter')

'''
address = 0x38

i2c = []
for i in range(16):
    i2c.append(sca.i2c[i])

    i2c[i].write(address, 47)
    sleep(0.2)

    i2c[i].write(address + 1, 11)
    sleep(0.2)

    i2c[i].write(address + 2, 10)
    sleep(0.2)

    i2c[i].write(address, 47)
    sleep(0.2)

    i2c[i].write(address + 1, 11)
    sleep(0.2)

    i2c[i].read(address + 2)
    #input('press enter')
    #sca.i2c._read_enable_i2c()
    input('press enter')
'''

#i2c0 = sca.i2c[0]
#i2c1 = sca.i2c[1]

#input('press enter')

ddress0 = 0x28
address1 = 0x38

#i2c = []
#for i in range(16):
#    i2c.append(sca.i2c[i])
#    i2c[i].write(address1, 47)
#    input('press enter')

#i2c1.write(address1, 47)

#input('press enter')
#i2c0._read_control_register()
#i2c1._read_control_register()




#========read pin =====================
#input('press enter')
#sca.pin._read()

#for i in range(128):
#    i2c1.write(i, 47)
#    input('press enter')


'''
i2c0.write(address0, 47)
input('press enter')

i2c0.write(address0 + 1, 11)
input('press enter')

i2c0.write(address0 + 2, 8)
input('press enter')

i2c0.write(address0, 47)
input('press enter')

i2c0.write(address0 + 1, 11)
input('press enter')

i2c0.read(address0 + 2)
input('press enter')
'''

'''
i2c1.write(address1, 47)
input('press enter')

i2c1.write(address1 + 1, 11)
input('press enter')

i2c1.write(address1 + 2, 10)
input('press enter')

i2c1.write(address1, 47)
input('press enter')

i2c1.write(address1 + 1, 11)
input('press enter')

i2c1.read(address1 + 2)
input('press enter')
'''


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



#for i in range(16):
#    i2c.append(gbt_sca.i2c[i])
#    input('press enter')
#gbt_sca.pin._read_enable_gpio()
#input('press enter')

#roc = ROCv3(transport=i2c,
#      base_address=0x28,
#      name='roc',
#      reset_pin=0,
#      path_to_file='HGCROC3_I2C_params_regmap.csv')

#configuration = load_yaml('roc_test_config.yml')
#roc.configure(configuration)

##roc.read(configuration, from_hardware=True)


