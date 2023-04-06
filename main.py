# from ROCv3 import ROCv3
#from GBT_SCA import GBT_SCA
#from Transactor import Transactor
from SlowControl_Interface import SlowControl_Interface
# from Virtual_SlowControl_Interface import SlowControl_Interface
# from utils import load_yaml

# Instantiate the Interface that connects to the hardware.
sc_interface = SlowControl_Interface()

# Instantiate the Transactor(s).
# transactor = Transactor(sc_interface=sc_interface)

# Instantiate the GBT_SCA(s).
# gbt_sca = GBT_SCA(transactor=transactor)

#print([hex(val) for val in transactor.transaction])
# print(transactor.response)
# # Instantiate the I2C master(s).
# i2c = gbt_sca.i2c[0]
# i2c.set_speed(400)

# Instantiate pin(s).
# reset_pin = gbt_sca.pin[3]
# reset_pin.set_mode("out")
# reset_pin.write(1)
# print(reset_pin.mode)

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
