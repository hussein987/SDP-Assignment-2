# SDP-Assignment-2
This repository contains the implementation of the [2nd Assignment](https://hackmd.io/@gFZmdMTOQxGFHEFqqU8pMQ/S1cZqwefo) of Software-Design-with-Python course

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
