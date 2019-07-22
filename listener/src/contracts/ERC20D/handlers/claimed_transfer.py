import web3
from contracts.event import EventHandler
from models import Commit
# import utils


class ClaimedTransfer(EventHandler):
    signature = "ClaimedTransfer(address,address,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    # def _normalize(self):
    #     self._args["_id"] = utils.add_0x_prefix(self._args["_id"].hex())

    def handle(self):
        commit = Commit()

        commit.opcode = "claimed_transfer_ERC20D"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._address

        data = {
            "from": self._args.get("_from"),
            "to": self._args.get("_to"),
            "value": self._args.get("_value"),
            "contractAddress": self._address
        }

        commit.data = data

        return [commit]
