

class Proposal:

    def __init__(self, pid: str, loan_value: float, monthly_installments: int):
        """

        :param pid:
        :param loan_value:
        :param monthly_installments:
        """

        self.pid = pid
        self.loan_value = loan_value
        self.monthly_installments = monthly_installments

    def validate_loan_value(self) -> bool:

        if self.loan_value < 30000.00 or self.loan_value > 3000000.00:
            return False
        return True

    def get_monthly_installment_value(self) -> float:

        return round(self.loan_value / self.monthly_installments, 2)

    def get_installments_in_years(self) -> int:

        return int(self.monthly_installments / 12)

    def check_proposal_payment_range(self) -> bool:

        years = self.get_installments_in_years()

        if 2 <= years <= 15:
            return True
        return False
