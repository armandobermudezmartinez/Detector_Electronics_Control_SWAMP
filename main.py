from ROCv3 import ROCv3
from SCA_GPIO import SCA_GPIO, GPIO
from SCA_I2C import SCA_I2C, I2C
from GBT_SCA import GBT_SCA
from Transactor import Transactor
from Transactor_Interface import Transactor_Interface
from utils import load_yaml

#######################################
############# Transactor ##############
#######################################

# Instantiate the Transactor(s) Interface.
transactor_interface = Transactor_Interface()

# Instantiate the Transactor(s).
transactor = Transactor(transactor_interface=transactor_interface)

#######################################
############# GBT_SCA #################
#######################################

# Instantiate the GBT_SCA(s).
gbt_sca = GBT_SCA(transactor=transactor)

############# GBT_SCA GPIOs ###########

# Instantiate the GBT_SCA GPIO block.
sca_gpio = SCA_GPIO(gbt_sca=gbt_sca, number_of_pins=1)

# Instantiate the GPIO(s).
reset_pin = GPIO(sca_gpio=sca_gpio, pin=0, mode=1)

############# GBT_SCA I2Cs #############

# Instantiate the GBT_SCA I2C block.
sca_i2c = SCA_I2C(gbt_sca=gbt_sca, number_of_masters=1)

# Instantiate the I2C master(s).
i2c = I2C(sca_i2c=sca_i2c, index=0, bus_frequency=400)

#######################################
############# ROC #####################
#######################################

# Instantiate the ROC(s)
roc = ROCv3(transport=i2c,
            bus=0,
            base_address=0,
            name='roc',
            reset_pin=reset_pin,
            path_to_file="HGCROC3_I2C_params_regmap.csv")

# Configure the ROC(s)
configuration = load_yaml('roc_test_config.yml')
roc.configure(configuration)

#######################################
############# Send Transactions #######
#######################################

transactor_interface.send_receive()

# print(transactor_interface.number_of_transactions)

# print(transactor_interface.transaction)
# for i in range(int(len(transactor_interface.transaction)/4)):
#     decoded_data = transactor._tx_decode(
#         transactor_interface.transaction[4*i:4*(i+1)])
#     print(decoded_data)
#     print(transactor._tx_encode(**decoded_data))
