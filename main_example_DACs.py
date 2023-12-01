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

# Instantiate the GPIO(s).
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

## Switch on the LDOs to power the HGCROC.
pin[22].write(1)
pin[23].write(1)

## Need to wait some time for the LDO to power on
sleep(1)

## Set the SOFT_RSTB and I2C_RSTB to 1, which means "no reset"
pin[2].write(1)
pin[3].write(1)

pin[7].write(1)
pin[8].write(0)
pin[9].write(0)
pin[10].write(0)
pin[11].write(0)
pin[12].write(0)
pin[13].write(0)
pin[14].write(0)
pin[15].write(0)


# Instantiate the DAC(s).

dac = []
for i in range(4):
    dac.append(sca.dac[i])

dac[0].write(0.613)
dac[0].read()
input('press enter')
dac[1].write(0.613)
dac[1].read()
input('press enter')
dac[2].write(0.686)
dac[2].read()
input('press enter')
dac[3].write(0.613)
dac[3].read()
input('press enter')