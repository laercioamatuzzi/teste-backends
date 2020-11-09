from distutils.util import strtobool
from model.proponent import Proponent
from model.warranty import Warranty
from model.proposal import Proposal
from utils.custom_exceptions import InvalidProposalException


class Event:

    def __init__(self, pid: int, events: list):

        self.pid = pid
        self.proposal = None
        self.main_proponent = None
        self.warrantys = []
        self.proponents = []
        self.events = events

    def prepare(self):
        """
        Prepare all the events messages, before process then
        :return:
        """

        processed_event_id = []

        for event in self.events:

            event_values = event.split(",")

            event_id = event_values[0]
            event_schema = event_values[1].lower()
            event_action = event_values[2].lower()
            event_timestamp = event_values[3]
            proposal_id = event_values[4]

            if event_id not in processed_event_id:

                processed_event_id.append(event_id)

                if event_schema == "proposal":

                    if event_action in ["created", "updated"]:

                        loan_value = float(event_values[5])
                        monthly_installments = int(event_values[6])

                        self.create_or_update_proposal(pid=proposal_id,
                                                       loan_value=loan_value,
                                                       monthly_installments=monthly_installments)

                elif event_schema == "warranty":

                    if event_action in ["added", "updated"]:

                        warranty_id = event_values[5]
                        warranty_value = float(event_values[6])
                        warranty_province = event_values[7]

                        self.create_or_update_warranty(wid=warranty_id,
                                                       pid=proposal_id,
                                                       value=warranty_value,
                                                       province=warranty_province)

                elif event_schema == "proponent":

                    if event_action in ["added", "updated"]:

                        proponent_id = event_values[5]
                        proponent_name = event_values[6]
                        proponent_age = int(event_values[7])
                        proponent_monthly_income = float(event_values[8])
                        proponent_is_main = strtobool(event_values[9])

                        self.create_or_update_proponent(prid=proponent_id,
                                                        pid=proposal_id,
                                                        name=proponent_name,
                                                        age=proponent_age,
                                                        monthly_income=proponent_monthly_income,
                                                        is_main=proponent_is_main,
                                                        event_action=event_action)

        self.check_and_remove_deleted_events()

    def validate(self) -> str:
        """
        Validate every Rule to check if a Proposal is valid or not
        if a single rule is not satisfied, a exception is raised and return a blank string
        :return: blank or proposal_id
        """

        installment_value = self.proposal.get_monthly_installment_value()

        try:
            if not self.proposal.validate_loan_value():
                raise InvalidProposalException
            if not self.proposal.check_proposal_payment_range():
                raise InvalidProposalException
            elif not self.get_proponent_quantity() >= 2:
                raise InvalidProposalException
            elif not self.set_main_proponent() == 1:
                raise InvalidProposalException
            elif not self.validate_proponents_age(age=18):
                raise InvalidProposalException
            elif not self.get_warranty_quantity() >= 1:
                raise InvalidProposalException
            elif not self.get_warrantys_total_value() >= (self.proposal.loan_value * 2):
                raise InvalidProposalException
            elif not self.validate_warrantys_province():
                raise InvalidProposalException
            elif not self.main_proponent.check_for_necessary_monthly_income_by_age(installment_value=installment_value):
                raise InvalidProposalException

            return self.proposal.pid

        except InvalidProposalException:
            return ""

    def check_and_remove_deleted_events(self):

        for event in self.events:

            event_values = event.split(",")
            event_schema = event_values[1].lower()
            event_action = event_values[2].lower()

            if event_schema == "warranty":

                if event_action == "removed":
                    warranty_id = event_values[5]
                    self.remove_warranty(wid=warranty_id)

    def create_or_update_proposal(self, pid: str, loan_value: float, monthly_installments: int):

        self.proposal = Proposal(pid=pid, loan_value=loan_value, monthly_installments=monthly_installments)

    def create_or_update_warranty(self, wid: str, pid: str, value: float, province: str):

        warranty = Warranty(wid=wid, pid=pid, value=value, province=province)
        self.warrantys.append(warranty)

    def remove_warranty(self, wid: str):

        for warranty in self.warrantys:
            if warranty.wid == wid:
                self.warrantys.remove(warranty)

    def create_or_update_proponent(self, prid: str, pid: str, name: str, age: int,
                                   monthly_income: float, is_main: bool, event_action: str):

        if event_action == "added":
            proponent = Proponent(prid=prid, pid=pid, name=name, age=age, monthly_income=monthly_income, is_main=is_main)
            self.proponents.append(proponent)

        elif event_action == "updated":

            for proponent in self.proponents:
                if proponent.prid == prid:
                    proponent.name = name
                    proponent.age = age
                    proponent.monthly_income = monthly_income
                    proponent.is_main = is_main

    def get_proponent_quantity(self):

        return len(self.proponents)

    def set_main_proponent(self) -> int:
        """
        set the main proponent to this event and return the total of main proponents found
        :return:
        """

        main_proponent_quantity = 0
        for proponent in self.proponents:

            if proponent.is_main:
                self.main_proponent = proponent
                main_proponent_quantity += 1

        return main_proponent_quantity

    def validate_proponents_age(self, age=18):

        for proponent in self.proponents:
            if proponent.is_under_age(age=age):
                return False

        return True

    def get_warranty_quantity(self):

        return len(self.warrantys)

    def get_warrantys_total_value(self):

        total = 0.0
        for warranty in self.warrantys:

            total += warranty.value

        return total

    def validate_warrantys_province(self):

        for warranty in self.warrantys:
            if not warranty.is_valid_province():
                return False

        return True
