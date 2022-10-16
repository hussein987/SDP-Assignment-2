class Room:
    def __init__(self, capacity: int, number: int, air_conditioned: bool):
        self.capacity = capacity
        self.number = number
        self.air_conditioned = air_conditioned
        self.activity_names = []
        self.activity_intervals = []

    def _check_interval(self, new_interval):
        if new_interval[0] < 800 or new_interval[1] > 2100:
            return False

        for interval in self.activity_intervals:
            if interval[0] < new_interval[0] < interval[1]:
                return False
            if interval[0] < new_interval[1] < interval[1]:
                return False
        return True

    def add_activity(self, activity_name: str, activity_interval: list) -> bool:
        if not self._check_interval(activity_interval):
            print("Can't add this activity, there is a conflict with it")
            return False

        self.activity_names.append(activity_name)
        self.activity_intervals.append(activity_interval)
        return True

    def __str__(self) -> str:
        ret = f"{self.number}\n\
        \t\tCapacity: {self.capacity}\n\
        \t\tAir conditioned: {self.air_conditioned}\n"
        if len(self.activity_names) > 0:
            ret += "\t\t\tactivities:\n"
            for name, interval in zip(self.activity_names, self.activity_intervals):
                ret += f"\t\t\t\t{name}: from {interval[0]} to {interval[1]}\n"
        return ret

    def get_capacity(self):
        return self.capacity

    def set_capacity(self, capacity: int):
        self.capacity = capacity

    def get_number(self):
        return self.number

    def set_number(self, number: int):
        self.number = number

    def get_air_conditioned(self):
        return self.air_conditioned

    def set_air_conditioned(self, air_conditioned: bool):
        self.air_conditioned = air_conditioned

    def get_activities(self):
        return (self.activity_names, self.activity_intervals)


class Klassroom(Room):
    def __str__(self) -> str:
        ret = super().__str__()
        ret = "\t\tklassroom " + ret
        return ret


class LectureAuditorium(Room):
    def __str__(self) -> str:
        ret = super().__str__()
        ret = "\t\tLectureAuditorium " + ret
        return ret
