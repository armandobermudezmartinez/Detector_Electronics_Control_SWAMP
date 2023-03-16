import concurrent.futures
import time
import tx_field


class Transactor_Interface:
    def __init__(self):
        self.transaction = []
        self.number_of_transactions = 0
        self.response = []
        self.number_of_received_transactions = -1
        self.free_transaction_ids = list(range(1, 1025))

    def _add_transaction(self, transaction):
        self.transaction += transaction
        self.number_of_transactions += 1

    def _send(self):
        with open('somefile.txt', 'w') as file:
            transaction = ''
            for i, value in enumerate(self.transaction):
                time.sleep(0.1)
                print("sending word", f'0x{value:08x}')
                transaction += f'0x{value:08x}' + '\t'
                if (i + 1) % 4 == 0:
                    transaction += '\n'
                    file.write(transaction)
                    file.flush()
                    transaction = ''

    def _receive(self):
        start_time = time.time()
        while True:
            print(
                f"awaiting complete response ... (received_transactions: {self.number_of_received_transactions})")
            time.sleep(0.5)
            with open('somefile.txt', 'r') as file:
                content = file.read()
                self.number_of_received_transactions = int(
                    len(content.split())/4)
                if self.number_of_transactions and self.number_of_received_transactions == self.number_of_transactions:
                    print("Received", self.number_of_received_transactions,
                          "Transactions:")
                    content = content.split()
                    data = [int(x, 0) for x in content]
                    for i in range(self.number_of_received_transactions):
                        decoded_data = self._tx_decode(data[4*i:4*(i+1)])
                        self.free_transaction_ids.append(
                            decoded_data['trans_id'])
                        print(decoded_data)
                    break
                if time.time() - start_time > 60:
                    print("Timeout!")
                    print("Read ", self.number_of_received_transactions, "Transactions. Expected",
                          self.number_of_transactions, "Transactions")
                    break

    def send_receive(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self._send)
            executor.submit(self._receive)

    def _tx_decode(self, encoded_data):
        bst_address = (encoded_data[3] << 8)
        bst_address += (encoded_data[2] >>
                        (tx_field.BROADCAST_ADDR["OFFSET"] % 32))
        repl_address = (encoded_data[2] >> (
            tx_field.REPLY_ADDR["OFFSET"] % 32)) & tx_field.REPLY_ADDR["MASK"]
        cmd_id = (encoded_data[2] >> (
            tx_field.COMMAND_ID["OFFSET"] % 32)) & tx_field.COMMAND_ID["MASK"]
        sca_address = (encoded_data[1] >> (
            tx_field.SCA_ADDR["OFFSET"] % 32)) & tx_field.SCA_ADDR["MASK"]
        trans_id = (encoded_data[1] >> (
            tx_field.TRANSACTION_ID["OFFSET"] % 32)) & tx_field.TRANSACTION_ID["MASK"]
        ch_address = (encoded_data[1] >> (
            tx_field.CHANNEL_ADDR["OFFSET"] % 32)) & tx_field.CHANNEL_ADDR["MASK"]
        cmd = (encoded_data[1] >> (tx_field.COMMAND["OFFSET"] %
               32)) & tx_field.COMMAND["MASK"]
        payload = encoded_data[0]

        field_dict = {'bst_address': bst_address, 'repl_address': repl_address, 'cmd_id': cmd_id,
                      'sca_address': sca_address, 'trans_id': trans_id, 'ch_address': ch_address,
                      'cmd': cmd, 'payload': payload}

        return field_dict


# transactor_interface = Transactor_Interface()
# transactor_interface.number_of_transactions = 11
# transactor_interface._receive()
