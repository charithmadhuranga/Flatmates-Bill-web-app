class Bill:
    """ "
    Object that contains information about a bill
    """

    def __init__(self, amount, period):
        self.amount = amount
        self.period = period


class Flatmate:
    """
    Object that contains information about a flatmate
    """

    def __init__(self, name, days_in_house):
        self.name = name
        self.days_in_house = days_in_house

    def pays(self, bill, flatmate2):
        return round(
            bill.amount
            * (self.days_in_house / (self.days_in_house + flatmate2.days_in_house)),
            2,
        )
