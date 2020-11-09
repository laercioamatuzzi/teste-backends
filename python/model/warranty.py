

class Warranty:

    def __init__(self, wid: str, pid: str, value: float, province: str):
        """

        :param wid: Warranty id
        :param pid: Proposal id
        :param value: Warranty value
        :param province: Warranty province
        """

        self.wid = wid
        self.pid = pid
        self.value = value
        self.province = province

    def is_valid_province(self) -> bool:
        """

        :return:
        """

        return self.province not in ["PR", "SC", "RS"]
