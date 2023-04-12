import uhal
import logging
# import tx_field
# import rx_field


class SlowControl_Interface:
    def __init__(self, connection='file:///opt/cms-hgcal-firmware/hgc-test-systems/active/uHAL_xml/connection.xml', device='mylittlememory'):
        logging.basicConfig(filename='test.log',
                            level=logging.INFO, format='%(levelname)s:%(message)s')

        self.connection = connection
        man = uhal.ConnectionManager(self.connection)
        devices = man.getDevices()

        if len(devices):
            logging.info(f'Found {len(devices)} device(s): {devices}')
        else:
            raise Exception("No device found")

        if device in devices:
            logging.info(
                f'Using device {device}')
            self.device = man.getDevice(device)
        else:
            logging.warning(
                f'Device {device} not among devices available, instead using {devices[0]}')
            self.device = man.getDevice(devices[0])

        logging.info(f'Nodes: {self.device.getNodes()}')

        self._reset_slow_control()

        sca_control = self.device.getNode("config.SCA_Control0").read()
        ic_control = self.device.getNode("config.IC_Control0").read()
        sca_status = self.device.getNode("config.SCA_Status0").read()
        ic_status = self.device.getNode("config.IC_Status0").read()

        logging.info(
            f'Reading registers: sca control: {sca_control}, ic control: {ic_control}, sca status: {sca_status}, ic status: {ic_status}')

        clk_speed = self.device.getNode("AXI_GPIO.Clk40_Freq").read()
        clk_speed = int(int(clk_speed)/1e+06)
        logging.info(f'Frequency of Slow Control: {clk_speed} MHz')
        if clk_speed != 40:
            logging.error(
                "Frequency of Slow Control clk not 40 MHz")
            raise Exception("Frequency of Slow Control clk not 40 MHz")

        self._clean_ic_rx_buffer()
        self._lpgbt_reset_rx()
        self._lpgbt_read_ready()
        self._lpgbt_transmit_ready()

        self.message = []
        self.response = []

    def _reset_slow_control(self):
        logging.info('Resetting Slow Control')
        self.device.getNode("config.ResetN.rstn").write(0x0)
        self.device.getNode("config.ResetN.rstn").write(0x1)

    def _clean_ic_rx_buffer(self):
        logging.info('Cleaning IC RX buffer')
        self.device.getNode("data.IC_RX_BRAM0.Data").writeBlock(
            [0, 0, 0, 0] * 1024)

    def _lpgbt_reset_rx(self):
        logging.info('Resetting lpGBT RX')
        self.device.getNode("lpGBT_GPIO.ResetRX").write(0x1)
        self.device.getNode("lpGBT_GPIO.ResetRX").write(0x0)

    def _lpgbt_read_ready(self):
        data = self.device.getNode("lpGBT_GPIO.Ready").read()
        if data == 0x0:
            logging.warning('Neither RX or TX ready')
        elif data == 0x1:
            logging.warning('Only RX ready')
        elif data == 0x2:
            logging.warning('Only TX ready')
        elif data == 0x3:
            logging.info('Both RX and TX ready')
        else:
            logging.error('Unexpected behavior')
            raise Exception(
                'Unexpected behavior while checking if the lpGBT is ready')

    def _lpgbt_transmit_ready(self):
        message = [0x00000010, 0x00000000, 0xE000CF01, 0x00010000,
                   0x00000002, 0x00000000, 0xE000EC01, 0x00010000,
                   0x000000E1, 0x00000000, 0xE000AC01, 0x00010000,
                   0x00000039, 0x00000000, 0xE000A601, 0x00010000,
                   0x00000006, 0x00000000, 0xE000FB01, 0x00010000]
        self._send(message, type='ic')
        self._receive(type='ic')

    def flush(self):
        self._send(self.message)
        return self._receive()

    def _send(self, message, type='sca'):
        self.number_of_transactions = int(len(message) / 4)
        if type == 'sca':
            self.device.getNode("data.SCA_TX_BRAM0.Data").writeBlock(message)
            self.device.getNode("config.SCA_Control0.NbrTransactions").write(
                self.number_of_transactions)
            self.device.getNode("config.SCA_Control0.Start").write(0x0)
            self.device.getNode("config.SCA_Control0.Start").write(0x1)

        elif type == 'ic':
            self.device.getNode(
                "data.IC_TX_BRAM0.Data").writeBlock(message)
            self.device.getNode("config.IC_Control0.NbrTransactions").write(
                self.number_of_transactions)
            self.device.getNode("config.IC_Control0.Start").write(0x0)
            self.device.getNode("config.IC_Control0.Start").write(0x1)

    def _receive(self, type='sca'):
        response = []
        if type == 'sca':
            while 1:
                if self.device.getNode("config.SCA_Status0.Busy").read() == 0:
                    break
            data = self.device.getNode("data.SCA_RX_BRAM0.Data").readBlock(
                self.number_of_transactions*4)
                    
            if self.device.getNode("config.SCA_Status0.zero_cmd").read() == 1:
                #print("Asked for 0 transactions.")
                logging.error(
                    'Asked for 0 transactions')

            if self.device.getNode("config.SCA_Status0.TimeoutN").read() != 1:
                #print("Timeout ok")
                logging.error('Timeout!')
                raise Exception('Timeout!')
            else:
                logging.info("Timeout Ok")
            logging.info(f'Number of Successful transactions: {self.device.getNode("config.SCA_Status0.NbrTransactions").read()}')

        elif type == 'ic':
            while 1:
                if self.device.getNode("config.IC_Status0.Busy").read() == 0:
                    break
            data = self.device.getNode(
                "data.IC_RX_BRAM0.Data").readBlock(self.number_of_transactions*4)
            logging.info(
                f'Number of successful transactions {self.device.getNode("config.IC_Status0.NbrTransactions").read()}')

            if self.device.getNode("config.IC_Status0.zero_cmd").read() == 1:
                logging.error(
                    'Asked for 0 transactions in lpGBT configuration')
                raise Exception(
                    'Asked for 0 transactions in lpGBT configuration')
            if self.device.getNode("config.IC_Status0.TimeoutN").read() != 1:
                logging.error('Timeout in lpGBT configuration')
                raise Exception('Timeout in lpGBT configuration')

        return data

#sc = SlowControl_Interface()
#
#data = [0x00000000, 0x00010000, 0x01000002, 0x00000000,
#        0x00000000, 0x00020000, 0x01000001, 0x00000000,
#        0x10000000, 0x00030006, 0x01000004, 0x00000000]
#sc.message = data
#response = sc.flush()

#from Transactor import Transactor
#transactor = Transactor()

#received_data = []
#for j in range(3):
#     for i in range(4):
#          received_data += [response[4*j+3-i]]
#print([hex(val) for val in response])
#print([hex(val) for val in data])
#print(data)
#print([hex(val) for val in received_data])
#for j in range(3):
#     decoded_data = transactor.gbtsca_rx_decode(received_data[4*j: 4*(j+1)])
#     print(decoded_data)


