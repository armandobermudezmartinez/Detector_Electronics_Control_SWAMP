import uhal
import rx_field


class Transactor_Interface:
    def __init__(self, connection=None, device=None):
        if connection == None:
            self.connection = "file:///opt/cms-hgcal-firmware/hgc-test-systems/active/uHAL_xml/connection.xml"
        else:
            self.connection = connection

        man = uhal.ConnectionManager(self.connection)
        if device == None:
            self.device = man.getDevice("mylittlememory")
        else:
            self.device = man.getDevice(device)

        self.ResetSlowControl()
        self.lpGBTResetRX()
        self.lpGBTReadReady()

        self.transaction = []
        self.number_of_transactions = 0
        self.response = None

    def _lpGBTReadReady(self):
        data = self.dev.getNode("lpGBT_GPIO.Ready").read()
        if data == 0x0:
            print("Neither RX or TX ready")
        elif data == 0x1:
            print("Only RX ready")
        elif data == 0x2:
            print("Only TX ready")
        elif data == 0x3:
            print("Both RX and TX ready")
        else:
            print("Unexpected behavior\n")

    def _ResetSlowControl(self):
        self.dev.getNode("config.ResetN.rstn").write(0x0)
        self.dev.getNode("config.ResetN.rstn").write(0x1)

    def _lpGBTResetRX(self):
        self.dev.getNode("lpGBT_GPIO.ResetRX").write(0x1)
        self.dev.getNode("lpGBT_GPIO.ResetRX").write(0x0)

    def _add_transaction(self, transaction):
        self.transaction += transaction
        self.number_of_transactions += 1

    def _send(self, transactions):
        self.dev.getNode("data.SCA_TX_BRAM0.Data").writeBlock(transactions)
        self.dev.getNode("config.SCA_Control0.NbrTransactions").write(
            self.number_of_transactions)
        self.dev.getNode("config.SCA_Control0.Start").write(0x1)
        self.dev.getNode("config.SCA_Control0.Start").write(0x0)

    def _receive(self):
        while True:
            if self.dev.getNode("config.SCA_Status0.Busy").read() == 0:
                break
        if self.dev.getNode("config.SCA_Status0.TimeoutN").read() == 0:
            print("Timeout!")
        self.response = self.dev.getNode("data.SCA_RX_BRAM0.Data").readBlock(
            self.number_of_transactions*4)

    def send_receive(self):
        self._send(self.transaction)
        self._receive()

        for i in range(self.number_of_transactions):
            decoded_data = self._rx_decode(self.response[4*i: 4*(i+1)])
            print(decoded_data)

    def _rx_decode(self, encoded_data):
        error_flag = ((encoded_data[2]) >> (
            rx_field.ERROR_FLAGS["OFFSET"] % 32)) & rx_field.ERROR_FLAGS["MASK"]
        sca_address = ((encoded_data[2]) >> (
            rx_field.SCA_ADDR["OFFSET"] % 32)) & rx_field.SCA_ADDR["MASK"]
        ctrl = ((encoded_data[2]) >> (
            rx_field.CONTROL["OFFSET"] % 32)) & rx_field.CONTROL["MASK"]
        trans_id = ((encoded_data[1]) >> (
            rx_field.TRANSACTION_ID["OFFSET"] % 32)) & rx_field.TRANSACTION_ID["MASK"]
        ch_address = ((encoded_data[1]) >> (
            rx_field.CHANNEL_ADDR["OFFSET"] % 32)) & rx_field.CHANNEL_ADDR["MASK"]
        nbytes = ((encoded_data[1]) >> (
            rx_field.NBYTES_PAYLOAD["OFFSET"] % 32)) & rx_field.NBYTES_PAYLOAD["MASK"]
        error = (encoded_data[1] >> (
            rx_field.ERROR["OFFSET"] % 32)) & rx_field.ERROR["MASK"]
        payload = encoded_data[0]

        received_dict = {'error_flag': error_flag,
                         'sca_address': sca_address,
                         'ctrl': ctrl,
                         'trans_id': trans_id,
                         'ch_address': ch_address,
                         'nbytes': nbytes,
                         'error': error,
                         'payload': payload
                         }

        return received_dict


# transactor_interface = Transactor_Interface()
# transactor_interface.number_of_transactions = 11
# transactor_interface._receive()