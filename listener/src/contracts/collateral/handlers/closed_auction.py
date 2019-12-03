import web3
from contracts.event import EventHandler
from models import Commit


class ClosedAuction(EventHandler):
    signature = "ClosedAuction(uint256,uint256,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "closed_auction"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction
        commit.address = self._tx.get("from")

        collateral = Collateral.objects.get(id=data["id"])
        loan = Loan.objects.get(id=collateral.debt_id)
        if loan.status == "2":
            status = str(CollateralState.TO_WITHDRAW.value)
        else:
            status = str(CollateralState.STARTED.value)

        data = {
            "id": str(self._args.get("_entryId")),
            "received": self._args.get("_received"),
            "leftover": self._args.get("_leftover"),
            "status": status
        }

        commit.data = data

        return [commit]
