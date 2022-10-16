from EdInstitution import EdInstitution


def get_uni(universities):
    universities_names = [university.name for university in universities]
    name = input("Enter institution name:\n")
    if name not in universities_names:
        print("Institution not found!!")
        print("Available institutions:\n", *universities_names)
        return None
    university_idx = universities_names.index(name)
    return universities[university_idx]


def get_room_idx(uni, room_type):
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


def add_room(universities):
    uni = get_uni(universities)
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

    uni.add_room(
        room_type=room_type,
        capacity=capacity,
        number=number,
        air_conditioned=air_conditioned,
    )
    print(f"{room_type} succesfully added to {uni.name}\n")


def print_institution(universities):
    uni = get_uni(universities)
    if uni is None:
        return

    print(uni, "\n")


def assign_activity(universities, room_type):
    uni = get_uni(universities)
    if uni is None:
        return
    room_idx = get_room_idx(uni, room_type)
    if room_idx is None:
        return

    activity_name = input("Enter activity name:\n")
    activity_interval = input("Enter activity interval in military time:\n")
    activity_interval = [int(interval) for interval in activity_interval.split()]

    uni.add_activity(room_type, room_idx, activity_name, activity_interval)


if __name__ == "__main__":
    universities = []
    while True:
        command = int(
            input(
                "Choose one operation from below :\n\
            1 : Add an institution\n\
            2 : Add classroom or Auditorium to institution\n\
            3 : Print institution summary\n\
            4 : Assign activity to classroom\n\
            5 : Assign activity to LectureAuditorium\n\
            6 : Exit program\n"
            )
        )
        if command == 1:
            name = input("Enter institution name:\n")
            universities.append(EdInstitution(name=name))
            print("Institution succesfully added\n")
        elif command == 2:
            add_room(universities)
        elif command == 3:
            print_institution(universities)
        elif command == 4:
            assign_activity(universities, "Classroom")
        elif command == 5:
            assign_activity(universities, "Auditorium")
        elif command == 6:
            break

    print("In database you have:")
    for uni in universities:
        print(uni, "\n\n")
