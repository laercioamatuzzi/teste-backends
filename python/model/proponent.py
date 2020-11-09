

class Proponent:

    def __init__(self, prid: str, pid: str, name: str, age: int, monthly_income: float, is_main: bool):
        """

        :param prid: Proponent id
        :param pid: Proposal id
        :param name: Proponent name
        :param age: Proponent age
        :param monthly_income: Proponent monthly incode
        :param is_main: check if is the main proponent
        """

        self.pid = pid
        self.prid = prid
        self.name = name
        self.age = age
        self.monthly_income = monthly_income
        self.is_main = is_main

    def is_under_age(self, age) -> bool:
        """

        :param age:
        :return:
        """
        return self.age < age

    def check_for_necessary_monthly_income_by_age(self, installment_value: float) -> bool:
        """

        :param installment_value:
        :return:
        """

        if 18 <= self.age <= 23:
            necessary_value = installment_value * 4
        elif 24 <= self.age <= 49:
            necessary_value = installment_value * 3
        else:
            necessary_value = installment_value * 2

        return self.monthly_income >= necessary_value
