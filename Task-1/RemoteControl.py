class Command:
    def get_uni(self, universities):
        universities_names = [university.name for university in universities]
        name = input("Enter institution name:\n")
        if name not in universities_names:
            print("Institution not found!!")
            print("Available institutions:\n", *universities_names)
            return None
        university_idx = universities_names.index(name)
        return universities[university_idx]

    def get_room_idx(self, uni, room_type):
        if room_type == "Classroom":
            rooms = uni.classrooms
        elif room_type == "Auditorium":
            rooms = uni.auditoriums

        number = int(input(f"Enter {room_type} number:\n"))
        numbers = [room.number for room in rooms]

        if number not in numbers:
            print("Room not found!!")
            print("Available rooms:\n", *numbers)
            return None
        room_idx = numbers.index(number)
        return room_idx

    def execute(self):
        pass


class AddRoom(Command):
    def execute(self, universities):
        uni = self.get_uni(universities)
        if uni is None:
            return

        command = int(input("Enter (1 for Classroom or 2 for Auditorium):\n"))
        if command not in [1, 2]:
            print("Invalid command\n")
            return

        args = input("Enter (capacity, number, air conditioner- yes/no):\n")
        capacity, number, air_conditioned = args.split()
        capacity = int(capacity)
        number = int(number)
        air_conditioned = True if air_conditioned == "yes" else False
        room_type = "Classroom" if command == 1 else "Auditorium"

        rooms = uni.classrooms if room_type == "Classroom" else uni.auditoriums
        numbers = [room.number for room in rooms]

        if number in numbers:
            print("This room already exists\n")
            return

        uni.add_room(
            room_type=room_type,
            capacity=capacity,
            number=number,
            air_conditioned=air_conditioned,
        )
        print(f"{room_type} succesfully added to {uni.name}\n")


class PrintInstitution(Command):
    def execute(self, universities):
        uni = self.get_uni(universities)
        if uni is None:
            return
        print(uni, "\n")


class ClassroomAssignActivity(Command):
    def execute(self, universities):
        uni = self.get_uni(universities)
        if uni is None:
            return
        room_idx = self.get_room_idx(uni, "Classroom")
        if room_idx is None:
            return

        activity_name = input("Enter activity name:\n")
        activity_interval = input("Enter activity interval in military time:\n")
        activity_interval = [int(interval) for interval in activity_interval.split()]

        uni.add_activity("Classroom", room_idx, activity_name, activity_interval)


class AuditoriumAssignActivity(Command):
    def execute(self, universities):
        uni = self.get_uni(universities)
        if uni is None:
            return
        room_idx = self.get_room_idx(uni, "Auditorium")
        if room_idx is None:
            return

        activity_name = input("Enter activity name:\n")
        activity_interval = input("Enter activity interval in military time:\n")
        activity_interval = [int(interval) for interval in activity_interval.split()]

        uni.add_activity("Auditorium", room_idx, activity_name, activity_interval)


class Remote:
    def __init__(self):
        self.slots = {}

    def set(self, cmd: Command, cmd_name: str):
        self.slots[cmd_name] = cmd

    def buttonWasPressed(self, cmd_name: int, universities):
        self.slots[cmd_name].execute(universities)
