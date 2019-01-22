import web3
from contracts.event import EventHandler
from models import Loan, Commit
from contracts.loanManager.loan_manager import loan_manager_interface


class Requested(EventHandler):
    signature = "Requested(bytes32,uint256)"
    signature_hash = web3.Web3.sha3(text=signature).hex()

    def _parse(self):
        self._id = self._event.get("topics")[1].hex()
        self._salt = int(self._event.get("data"), 16)
        self._block_number = self._event.get('blockNumber')
        self._transaction = self._event.get('transactionHash').hex()

    def handle(self):
        commit = Commit()

        commit.opcode = "requested_loan_manager"
        commit.timestamp = self._block_timestamp()
        commit.proof = self._transaction

        request_data = loan_manager_interface.get_request_data(self._id)
        print("requestData =", request_data)


        data = {
            "id": self._id,
            "open": True,
            "approved": request_data.get("creator") == request_data.get("borrower"),
            "position": "0",
            "expiration": str(request_data.get("expiration")),
            "amount": str(request_data.get("amount")),
            "cosigner": "0x0",
            "model": request_data.get("model"),
            "creator": request_data.get("creator"),
            "oracle": request_data.get("oracle"),
            "borrower": request_data.get("borrower"),
            "salt": str(self._salt),
            "loanData": request_data.get("loanData"),
            "created": str(self._block_timestamp()),
            "descriptor": request_data.get("descriptor"),
            "currency": request_data.get("currency"),
            "status": request_data.get("status")
        }

        commit.data = data

        return [commit]