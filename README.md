# SDP-Assignment-2
This repository contains the implementation of the [2nd Assignment](https://hackmd.io/@gFZmdMTOQxGFHEFqqU8pMQ/S1cZqwefo) of Software-Design-with-Python course

## Team:
Hussein Younes

Yusuf Mesbah

## Task 1
The **Remote control pattern** were used to execute the commands.  
### How to run:
Run this command in your terminal:
`python3 main.py`

### How to use:
When you run you will be givin options to add institutes, classes and activities.

When reqired to add mutible things in one prompet you should input them with
just 1 blank space in between, example:
```
Enter (capacity, number, air conditioner- yes/no):
30 312 yes
```

When required to enter time, we use military time, examples:
```
13:15 -> 1315
1:00 -> 0100
```
The institutes are automatically saved.
To load a previusly saved institute, just use the first command and add the
institute and it will be automatically loaded.

### Using Docker
To build the image: `docker image build -t sdpy:1 .`

To run the image: `docker run -i -t sdpy:1`


## Task 2

The task is to design and implement a system that will analyze cloud gaming users

### How to run:
python3 main.py

example:

```
$ python3 main.py
Choose one operation from below :
            1 : Get status for the past 7 days
            2 : Print user summary
            3 : Predict user next session duration
            4 : Fetch new data and update users data and ML model
            5 : Get top 5 users based on time spent gaming
            6 : Exit program
5
Rank                    User id                  Time spent gaming
0       7ccefde6-3a8b-469a-8cbd-401968f5ca98            99090.0 sec
1       413f3a66-ca86-4204-ab62-53a581d7495b            67365.0 sec
2       5be02825-fa61-4f81-a477-12cf0cc85782            60165.0 sec
3       299567d3-4d50-474a-a7c6-b021520a9dad            48990.0 sec
4       d316573a-46df-4c23-b404-dde8790096c6            48405.0 sec

Choose one operation from below :
            1 : Get status for the past 7 days
            2 : Print user summary
            3 : Predict user next session duration
            4 : Fetch new data and update users data and ML model
            5 : Get top 5 users based on time spent gaming
            6 : Exit program
6

Statistics for the past 7 days:

Total sessions : 551
Average time spent per session : 1.0 hrs : 1.0 minutes : 3.0 seconds
Sum of hours spent by all users : 560.0 hrs : 38.0 minutes : 35.0 seconds


Save summary ? (yes/no)
yes
Good bye!!
```