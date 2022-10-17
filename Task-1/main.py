from EdInstitution import EdInstitution
from RemoteControl import Remote
from RemoteControl import (
    AddRoom,
    PrintInstitution,
    ClassroomAssignActivity,
    AuditoriumAssignActivity,
)

if __name__ == "__main__":
    universities = []
    remote = Remote()
    remote.set(cmd=AddRoom(), cmd_name="AddRoom")
    remote.set(cmd=PrintInstitution(), cmd_name="PrintInstitution")
    remote.set(cmd=ClassroomAssignActivity(), cmd_name="ClassroomAssignActivity")
    remote.set(cmd=AuditoriumAssignActivity(), cmd_name="AuditoriumAssignActivity")

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
            remote.buttonWasPressed("AddRoom", universities)
        elif command == 3:
            remote.buttonWasPressed("PrintInstitution", universities)
        elif command == 4:
            remote.buttonWasPressed("ClassroomAssignActivity", universities)
        elif command == 5:
            remote.buttonWasPressed("AuditoriumAssignActivity", universities)
        elif command == 6:
            break

    print("In database you have:")
    for uni in universities:
        print(uni, "\n\n")
