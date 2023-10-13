import gbtsca_tx
import gbtsca_rx
from transactor_config import transactor_config as config


class Transactor:
    def __init__(self, sc_interface=0):
        self.sc_interface = sc_interface
        self.broadcast_address = config['bst_address']
        self.reply_address = config['repl_address']
        self.sca_address = config['sca_address']
        self.free_transaction_ids = list(range(1, 1025))
        self.transaction = []
        self.comments = []
        self.number_of_transactions = 0
        self.number_of_successful_transactions = 0

    def flush(self):
        self.response = []
        self.comments = []
        self.number_of_transactions = int(len(self.transaction)/4)
        self.sc_interface.message = self.transaction
        self.received_data, self.number_of_successful_transactions = self.sc_interface.flush()
        for i in range(self.number_of_transactions):
            decoded_data = self.gbtsca_rx_decode(
                self.received_data[4*i: 4*(i+1)])
            self.response += [decoded_data]
            if (decoded_data['trans_id']):
                self.free_transaction_ids.append(decoded_data['trans_id'])
        self.transaction = []

    def write(self, channel, command, command_id=0b100, mask=0, data=0, comment=''):
        if len(self.free_transaction_ids) == 0:
            raise Exception("No more free transaction IDs")
        self._transaction_id = self.free_transaction_ids.pop(0)
        masked_data = (~data & mask) | (data & mask)
        self.transaction += self.gbtsca_tx_encode(self.broadcast_address, self.reply_address, command_id,
                                                  self.sca_address, self._transaction_id, channel, command, masked_data)
        self.comments += [comment]

    def read(self):
        number_of_transactions = int(len(self.transaction)/4)
        decoded_transaction = []
        encoded_transaction = self.transaction
        comments = self.comments
        for i in range(number_of_transactions):
            decoded_transaction.append(self._gbtsca_tx_decode(
                self.transaction[4*i: 4*(i+1)]))
        self.flush()
        for i in range(number_of_transactions):
            print("Transaction:\n", decoded_transaction[i])
            print("Encoded Transaction:\n", encoded_transaction[4*i: 4*(i+1)])
            print("Response:\n", self.response[i])
            print("Comment:", comments[i])
        print(
            f"Number of Transactions: {number_of_transactions}, Number of Successful Transactions: {number_of_transactions}")
        print(120*"-")

    def gbtsca_tx_encode(self, bst_address, repl_address, cmd_id, sca_address, trans_id, ch_address, cmd, payload):
        out = (bst_address &
               gbtsca_tx.BROADCAST_ADDR["MASK"]) << gbtsca_tx.BROADCAST_ADDR["OFFSET"]
        out = out | (
            (repl_address & gbtsca_tx.REPLY_ADDR["MASK"]) << gbtsca_tx.REPLY_ADDR["OFFSET"])
        out = out | (
            (cmd_id & gbtsca_tx.COMMAND_ID["MASK"]) << gbtsca_tx.COMMAND_ID["OFFSET"])
        out = out | (
            (sca_address & gbtsca_tx.SCA_ADDR["MASK"]) << gbtsca_tx.SCA_ADDR["OFFSET"])
        out = out | (
            (trans_id & gbtsca_tx.TRANSACTION_ID["MASK"]) << gbtsca_tx.TRANSACTION_ID["OFFSET"])
        out = out | (
            (ch_address & gbtsca_tx.CHANNEL_ADDR["MASK"]) << gbtsca_tx.CHANNEL_ADDR["OFFSET"])
        out = out | (
            (cmd & gbtsca_tx.COMMAND["MASK"]) << gbtsca_tx.COMMAND["OFFSET"])
        out = out | (
            (payload & gbtsca_tx.PAYLOAD["MASK"]) << gbtsca_tx.PAYLOAD["OFFSET"])

        data = [(out >> i*32) & 0xFFFFFFFF for i in range(4)]

        return data

    def _gbtsca_tx_decode(self, encoded_data):
        bst_address = (encoded_data[3] << 8)
        bst_address += (encoded_data[2] >>
                        (gbtsca_tx.BROADCAST_ADDR["OFFSET"] % 32))
        repl_address = (encoded_data[2] >> (
            gbtsca_tx.REPLY_ADDR["OFFSET"] % 32)) & gbtsca_tx.REPLY_ADDR["MASK"]
        cmd_id = (encoded_data[2] >> (
            gbtsca_tx.COMMAND_ID["OFFSET"] % 32)) & gbtsca_tx.COMMAND_ID["MASK"]
        sca_address = (encoded_data[1] >> (
            gbtsca_tx.SCA_ADDR["OFFSET"] % 32)) & gbtsca_tx.SCA_ADDR["MASK"]
        trans_id = (encoded_data[1] >> (
            gbtsca_tx.TRANSACTION_ID["OFFSET"] % 32)) & gbtsca_tx.TRANSACTION_ID["MASK"]
        ch_address = (encoded_data[1] >> (
            gbtsca_tx.CHANNEL_ADDR["OFFSET"] % 32)) & gbtsca_tx.CHANNEL_ADDR["MASK"]
        cmd = (encoded_data[1] >> (gbtsca_tx.COMMAND["OFFSET"] %
               32)) & gbtsca_tx.COMMAND["MASK"]
        payload = encoded_data[0]

        field_dict = {'bst_address': bst_address, 'repl_address': repl_address, 'cmd_id': cmd_id,
                      'sca_address': sca_address, 'trans_id': trans_id, 'ch_address': ch_address,
                      'cmd': cmd, 'payload': payload}

        return field_dict

    def gbtsca_rx_decode(self, data):
        error_flag = ((data[2]) >> (
            gbtsca_rx.ERROR_FLAGS["OFFSET"] % 32)) & gbtsca_rx.ERROR_FLAGS["MASK"]
        sca_address = ((data[2]) >> (
            gbtsca_rx.SCA_ADDR["OFFSET"] % 32)) & gbtsca_rx.SCA_ADDR["MASK"]
        ctrl = ((data[2]) >> (
            gbtsca_rx.CONTROL["OFFSET"] % 32)) & gbtsca_rx.CONTROL["MASK"]
        trans_id = ((data[1]) >> (
            gbtsca_rx.TRANSACTION_ID["OFFSET"] % 32)) & gbtsca_rx.TRANSACTION_ID["MASK"]
        ch_address = ((data[1]) >> (
            gbtsca_rx.CHANNEL_ADDR["OFFSET"] % 32)) & gbtsca_rx.CHANNEL_ADDR["MASK"]
        nbytes = ((data[1]) >> (
            gbtsca_rx.NBYTES_PAYLOAD["OFFSET"] % 32)) & gbtsca_rx.NBYTES_PAYLOAD["MASK"]
        error = (data[1] >> (
            gbtsca_rx.ERROR["OFFSET"] % 32)) & gbtsca_rx.ERROR["MASK"]
        payload = data[0]

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
