import tx_field


class Transactor:
    def __init__(self, transactor_interface=0, broadcast_address=0, reply_address=0, sca_address=0):
        self.transactor_interface = transactor_interface
        self.broadcast_address = broadcast_address
        self.reply_address = reply_address
        self.sca_address = sca_address

    def write(self, channel, command, mask=0, data=0):
        if len(self.transactor_interface.free_transaction_ids) == 0:
            raise Exception("No more free transaction IDs")
        transaction_id = self.transactor_interface.free_transaction_ids.pop(0)
        command_id = 0b100

        transaction = self._tx_encode(self.broadcast_address, self.reply_address, command_id,
                                      self.sca_address, transaction_id, channel, command, data)
        self.transactor_interface._add_transaction(transaction)

    def _tx_encode(self, bst_address, repl_address, cmd_id, sca_address, trans_id, ch_address, cmd, payload):
        out = (bst_address &
               tx_field.BROADCAST_ADDR["MASK"]) << tx_field.BROADCAST_ADDR["OFFSET"]
        out = out | (
            (repl_address & tx_field.REPLY_ADDR["MASK"]) << tx_field.REPLY_ADDR["OFFSET"])
        out = out | (
            (cmd_id & tx_field.COMMAND_ID["MASK"]) << tx_field.COMMAND_ID["OFFSET"])
        out = out | (
            (sca_address & tx_field.SCA_ADDR["MASK"]) << tx_field.SCA_ADDR["OFFSET"])
        out = out | (
            (trans_id & tx_field.TRANSACTION_ID["MASK"]) << tx_field.TRANSACTION_ID["OFFSET"])
        out = out | (
            (ch_address & tx_field.CHANNEL_ADDR["MASK"]) << tx_field.CHANNEL_ADDR["OFFSET"])
        out = out | (
            (cmd & tx_field.COMMAND["MASK"]) << tx_field.COMMAND["OFFSET"])
        out = out | (
            (payload & tx_field.PAYLOAD["MASK"]) << tx_field.PAYLOAD["OFFSET"])

        data = [(out >> i*32) & 0xFFFFFFFF for i in range(4)]

        return data
