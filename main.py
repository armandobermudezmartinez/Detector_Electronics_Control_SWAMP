# from ROCv3 import ROCv3
from GBT_SCA import GBT_SCA
from Transactor import Transactor
from SlowControl_Interface import SlowControl_Interface
# from utils import load_yaml

# Instantiate the Interface that connects to the hardware.
sc_interface = SlowControl_Interface()

# Instantiate the Transactor(s).
transactor = Transactor(sc_interface=sc_interface)

# Instantiate the GBT_SCA(s).
gbt_sca = GBT_SCA(transactor=transactor)

transactor.read()

# Instantiate the I2C master(s).
i2c = []
for i in range(16):
    i2c.append(gbt_sca.i2c[i])

transactor.read()

gbt_sca.read_enable_i2c()
transactor.read()


# # Instantiate pin(s).
#pin = []
#for i in range(32):
#    pin.append(gbt_sca.pin[i])
#    if i % 2:
#        pin[i].set_mode('out')
#    else:
#        pin[i].set_mode('in')

#transactor.read()

#gbt_sca.read_gpio_mode()
#transactor.read()


# # Instantiate the ROC(s)
# roc = ROCv3(transport=i2c, bus=0, base_address=0, name='roc',
#             reset_pin=reset_pin, path_to_file="HGCROC3_I2C_params_regmap.csv")

# # Configure the ROC(s)
# configuration = load_yaml('roc_test_config.yml')
# roc.configure(configuration)

#######################################
############# Send Transactions #######
#######################################

# sc_interface.send_receive()

# # print(sc_interface.number_of_transactions)

# # print(sc_interface.transaction)
# # for i in range(int(len(sc_interface.transaction)/4)):
# #     decoded_data = transactor._tx_decode(
# #         sc_interface.transaction[4*i:4*(i+1)])
# #     print(decoded_data)
# #     print(transactor._tx_encode(**decoded_data))
