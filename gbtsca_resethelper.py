import time
from glob import glob
import gpiod
import uhal

class gbtsca_resethelper():
    def __init__(self, ipbushw, baseName):
        # check if gpio is supported by linux gpio driver
        # find reset gpio
        resetGPIOName = baseName+"_axi_gpio_0"
        gpioLabel = ""
        for gpiopath in glob("/sys/class/gpio/*"):
            try:
                with open(gpiopath + "/device/of_node/label") as f:
                    if resetGPIOName in f.read():
                        with open(gpiopath + "/label") as f_label:
                            gpioLabel = f_label.read().strip()
                            break
            except(IOError):
                pass

        if len(gpioLabel) > 0:
            for gpio in gpiod.chip_iter():
                if gpioLabel in gpio.label:
                    self.gpio_pin = gpio.get_line(0)
                    config = gpiod.line_request()
                    config.request_type = gpiod.line_request.DIRECTION_OUTPUT
                    self.gpio_pin.request(config, default_val=1)
                    self.reset_impl = self.reset_gpiod
                    break
        else:
            NODE_NAME = "_gpio"
            self.node = ipbushw.getNode(baseName+NODE_NAME)
            self.reset_impl = self.reset_uhal

    def reset(self):
        self.reset_impl()

    def reset_uhal(self):
        self.node.getNode("reset").write(0)
        self.node.getClient().dispatch()
        self.node.getNode("reset").write(1)
        self.node.getClient().dispatch()

    def reset_gpiod(self):
        self.gpio_pin.set_value(0)
        self.gpio_pin.set_value(1)


connection='file:///opt/cms-hgcal-firmware/hgc-test-systems/active/uHAL_xml/connections.xml'
device_name='TOP'

man = uhal.ConnectionManager(connection)
devices = man.getDevices()

if device_name in devices:
    device = man.getDevice(device_name)

device.getNode("Transactor-Slow-Control-0_config.ResetN.rstn").write(0x0)
device.getNode("Transactor-Slow-Control-0_config.ResetN.rstn").write(0x1)

print(device.getNodes())

#gbtsca_resethelper = gbtsca_resethelper(device, "gbt_sca_com_0")
#gbtsca_resethelper.reset()
