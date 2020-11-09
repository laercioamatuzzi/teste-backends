from controller.event_controller import EventController
import unittest
from utils.constants import *


class TestProposal(unittest.TestCase):

    def setUp(self) -> None:

        self.file = open(file="../test/input/input000.txt", mode="r")
        lines = self.file.readlines()
        number_of_events = len(lines)
        self.input = str(number_of_events) + "\n"
        self.input += "".join(lines)

        events = EventController.prepare_event_list(events=self.input)
        self.event = events[1]
        self.event.prepare()

    def tearDown(self) -> None:
        self.file.close()

    def test_proposal_loan_value_range(self):

        self.assertTrue(self.event.proposal.validate_loan_value())

    def test_loan_payment_years_range(self):

        self.assertTrue(self.event.proposal.check_proposal_payment_range())

    def test_proponent_quantity(self):

        self.assertGreaterEqual(self.event.get_proponent_quantity(), MIN_NEEDED_PROPONENT)

    def test_only_one_main_proponent(self):

        self.assertEqual(self.event.set_main_proponent(), MAX_MAIN_PROPONENT_ALLOWED)

    def test_proponents_under_age(self):

        self.assertTrue(self.event.validate_proponents_age(age=MIN_PROPONENT_AGE))

    def test_warranty_quantity(self):
        self.assertGreaterEqual(self.event.get_warranty_quantity(), MIN_NEEDED_WARRANTY)

    def test_warrantys_values_are_greater_then_doubled_loan_value(self):

        doubled_loan_value = self.event.proposal.loan_value * 2
        self.assertGreaterEqual(self.event.get_warrantys_total_value(), doubled_loan_value)

    def test_warrantys_valid_province(self):

        self.assertTrue(self.event.validate_warrantys_province())

    def test_main_proponent_necessary_monthly_income_value(self):

        monthly_installment_value = self.event.proposal.get_monthly_installment_value()
        self.event.set_main_proponent()
        proponent = self.event.main_proponent

        result = proponent.check_for_necessary_monthly_income_by_age(installment_value=monthly_installment_value)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
