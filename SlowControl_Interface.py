import uhal
import logging


class SlowControl_Interface:
    def __init__(self, connection='file:///opt/cms-hgcal-firmware/hgc-test-systems/active/uHAL_xml/connections.xml', device='TOP'):
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

        # logging.info(f'Nodes: {self.device.getNodes()}')

        self._reset_slow_control()

        sca_control = self.device.getNode("Transactor-Slow-Control-0_config.SCA_Control0").read()
        sca_status = self.device.getNode("Transactor-Slow-Control-0_config.SCA_Status0").read()

        logging.info(
            f'Reading registers: sca control: {sca_control}, sca status: {sca_status}')

        self._clean_ic_rx_buffer()

        self.message = []
        self.response = []

    def _reset_slow_control(self):
        logging.info('Resetting Slow Control')
        self.device.getNode("Transactor-Slow-Control-0_config.ResetN.rstn").write(0x0)
        self.device.getNode("Transactor-Slow-Control-0_config.ResetN.rstn").write(0x1)

    def _clean_ic_rx_buffer(self):
        logging.info('Cleaning IC RX buffer')
        self.device.getNode("Transactor-Slow-Control-0_data.IC_RX_BRAM0.Data").writeBlock(
            [0, 0, 0, 0] * 1024)

    def flush(self):
        self._send(self.message)
        return self._receive()

    def _send(self, message, type='sca'):
        self.number_of_transactions = int(len(message) / 4)
        if type == 'sca':
            self.device.getNode("Transactor-Slow-Control-0_data.SCA_TX_BRAM0.Data").writeBlock(message)
            self.device.getNode("Transactor-Slow-Control-0_config.SCA_Control0.NbrTransactions").write(
                self.number_of_transactions)
            self.device.getNode("Transactor-Slow-Control-0_config.SCA_Control0.Start").write(0x0)
            self.device.getNode("Transactor-Slow-Control-0_config.SCA_Control0.Start").write(0x1)

        elif type == 'ic':
            self.device.getNode(
                "Transactor-Slow-Control-0_data.IC_TX_BRAM0.Data").writeBlock(message)
            self.device.getNode("Transactor-Slow-Control-0_config.IC_Control0.NbrTransactions").write(
                self.number_of_transactions)
            self.device.getNode("Transactor-Slow-Control-0_config.IC_Control0.Start").write(0x0)
            self.device.getNode("Transactor-Slow-Control-0_config.IC_Control0.Start").write(0x1)

    def _receive(self, type='sca'):
        number_of_successful_transactions = 0
        if type == 'sca':
            while 1:
                if self.device.getNode("Transactor-Slow-Control-0_config.SCA_Status0.Busy").read() == 0:
                    break
            data = self.device.getNode("Transactor-Slow-Control-0_data.SCA_RX_BRAM0.Data").readBlock(
                self.number_of_transactions*4)
            number_of_successful_transactions = self.device.getNode("Transactor-Slow-Control-0_config.SCA_Status0.NbrTransactions").read()
            if self.device.getNode("Transactor-Slow-Control-0_config.SCA_Status0.zero_cmd").read() == 1:
                logging.error(
                    'Asked for 0 transactions')

            if self.device.getNode("Transactor-Slow-Control-0_config.SCA_Status0.TimeoutN").read() != 1:
                logging.error('Timeout!')
                raise Exception('Timeout!')
            else:
                logging.info("Timeout Ok")
            logging.info(f'Number of Successful transactions: {number_of_successful_transactions}')

        elif type == 'ic':
            while 1:
                if self.device.getNode("Transactor-Slow-Control-0_config.IC_Status0.Busy").read() == 0:
                    break
            data = self.device.getNode(
                "Transactor-Slow-Control-0_data.IC_RX_BRAM0.Data").readBlock(self.number_of_transactions*4)
            number_of_successful_transactions = self.device.getNode("Transactor-Slow-Control-0_config.IC_Status0.NbrTransactions").read()
            logging.info(
                f'Number of successful transactions {number_of_successful_transactions}')

            if self.device.getNode("Transactor-Slow-Control-0_config.IC_Status0.zero_cmd").read() == 1:
                logging.error(
                    'Asked for 0 transactions in lpGBT configuration')
                raise Exception(
                    'Asked for 0 transactions in lpGBT configuration')
            if self.device.getNode("Transactor-Slow-Control-0_config.IC_Status0.TimeoutN").read() != 1:
                logging.error('Timeout in lpGBT configuration')
                raise Exception('Timeout in lpGBT configuration')

        return data, number_of_successful_transactions

