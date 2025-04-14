class UserDTO:
    def __init__(self, chart_no, name, jno, mobile_no):
        self.chart_no = chart_no
        self.name = name
        self.jno = jno
        self.mobile_no = mobile_no

    def __eq__(self, other):
        if not isinstance(other, UserDTO):
            return False
        return (
            self.chart_no == other.chart_no and
            self.name == other.name and
            self.jno == other.jno and
            self.mobile_no == other.mobile_no
        )

    def __repr__(self):
        return f"UserDTO(chart_no={self.chart_no}, name={self.name}, jno={self.jno}, mobile_no={self.mobile_no})"
