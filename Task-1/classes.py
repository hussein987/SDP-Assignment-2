class EdInstitution:

    def __init__(self, name="IU", class_rooms=None, lectures=None, auditoriums=None):
        self.name = name
        self.class_rooms = class_rooms
        self.lectures = lectures
        self.auditoriums = auditoriums

    class Classroom:
        def __init__(self, capacity, number, air_conditioned, activities):
            self.capacity = capacity
            self.number = number
            self.air_conditioned = air_conditioned
            self.activities = activities

        class Activity:
            def __init__(self, start_time, end_time):
                self.time_interval = (start_time, end_time)

        def get(self, __name: str):
            return getattr(self, __name)

        def set(self, __name: str, __value) -> None:
            setattr(self, __name, __value)

    class LectureAuditorium(Classroom):
        def __init__(self):
            super().__init__()

    def get(self, __name: str):
        return getattr(self, __name)

    def set(self, __name: str, __value) -> None:
        setattr(self, __name, __value)

    def add(self):
        pass

    def remove(self):
        pass

    def saveToFile(self):
        pass

    def restoreFromFile(self):
        pass

    def print_classrooms(self):
        pass



    def __str__(self):
        return f"Here's the overloaded print function for the class {self.__class__.__name__}"