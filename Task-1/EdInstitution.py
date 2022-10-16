import os
import datetime
import pickle

from Rooms import Klassroom, LectureAuditorium


class EdInstitution:
    def __init__(self, name="IU"):
        self.name = name
        self.classrooms = []
        self.auditoriums = []
        if os.path.isfile(f"{self.name}.pkl"):
            self.restoreFromFile()

    def add_room(
        self, room_type: str, capacity: int, number: int, air_conditioned: bool
    ):
        if room_type == "Classroom":
            room = Klassroom(
                capacity=capacity, number=number, air_conditioned=air_conditioned
            )
            self.classrooms.append(room)
        elif room_type == "Auditorium":
            room = LectureAuditorium(
                capacity=capacity, number=number, air_conditioned=air_conditioned
            )
            self.auditoriums.append(room)

        self.saveToFile()

    def add_activity(
        self, room_type: str, room_idx: int, activity_name: str, activity_interval: list
    ):
        if room_type == "Classroom":
            rooms = self.classrooms
        elif room_type == "Auditorium":
            rooms = self.auditoriums
        rooms[room_idx].add_activity(activity_name, activity_interval)

        self.saveToFile()

    def remove(self, room_type: str, idx: int):
        if room_type == "Classroom":
            del self.classrooms[idx]
        elif room_type == "Auditorium":
            del self.auditoriums[idx]

        self.saveToFile()

    def __str__(self) -> str:
        ret = f"{self.name}:\n"
        ret += f"\tclassrooms : {len(self.classrooms)}\n"

        num_available_classrooms = 0
        num_available_auditoriums = 0
        now = datetime.datetime.now()
        current_time = now.hour * 100 + now.minute

        for room in self.classrooms:
            ret += room.__str__() + "\n"
            num_available_classrooms += room._check_interval(
                (current_time, current_time + 1)
            )

        ret += f"\tAuditorium(s) : {len(self.auditoriums)}\n"
        for room in self.auditoriums:
            ret += room.__str__() + "\n"
            num_available_auditoriums += room._check_interval(
                (current_time, current_time + 1)
            )

        ret += f"\tStatus for today (now: {current_time}) : {num_available_classrooms} available classroom(s) and {num_available_auditoriums} available auditorium(s)"

        return ret

    def saveToFile(self):
        with open(f"{self.name}.pkl", "wb") as file:
            pickle.dump(self, file)

    def restoreFromFile(self):
        with open(f"{self.name}.pkl", "rb") as file:
            uni = pickle.load(file)
        self.classrooms = uni.classrooms
        self.auditoriums = uni.auditoriums
