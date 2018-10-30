from contracts.event import EventHandler
import web3


class SetInterest(EventHandler):
    signature = "_setInterest(bytes32,uint128)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        pass

    def handle(self):
        return []