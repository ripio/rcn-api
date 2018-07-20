from graceful.resources.generic import RetrieveAPI
from graceful.resources.generic import PaginatedListCreateAPI
from graceful.parameters import StringParam
import falcon
from serializers import LoanSerializer
from models import Loan


class LoanList(PaginatedListCreateAPI):
    serializer = LoanSerializer()
    status = StringParam('Status filter')
    creator = StringParam("Creator filter")
    oracle = StringParam("Oracle filter")
    borrower = StringParam("Borrower filter")
    lender = StringParam("Borrower filter")
    cosigner = StringParam("Cosigner filter")
    approvedTransfer = StringParam("Approved Transfer filter")

    def list(self, params, meta, **kwargs):
        #  Filtering -> Ordering -> Limiting
        filter_params = params.copy()
        filter_params.pop("indent")
        page_size = filter_params.pop("page_size")
        page = filter_params.pop("page")
        offset = (page) * page_size

        return Loan.objects.filter(**filter_params).skip(offset).limit(page_size)

    def create(self, params, meta, validated, **kwargs):
        loan = Loan(**validated)
        loan.save()
        return loan


class LoanItem(RetrieveAPI):
    serializer = LoanSerializer()

    def retrieve(self, params, meta, loan_index, **kwargs):
        try:
            return Loan.objects.get(index=loan_index)
        except Loan.DoesNotExist:
            raise falcon.HTTPNotFound(
                title='Loan does not exists',
                description='Loan with index={} does not exists'.format(loan_index)
            )
