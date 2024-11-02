import threading, os
from shutil import posix
from threading import Thread
import time
from queue import Queue


seconds = 0
# Events to control thread behavior
system_event = threading.Event()
display_event = threading.Event()
roads = 0
interval = 0
circle = []
rotating_queue = []
timer = []
decrement = 0
counter = 1
op = 0
ANSI_RED = "\u001B[31m"
ANSI_GREEN = "\u001B[32m"
ANSI_YELLOW = "\u001B[33m"
ANSI_RESET = "\u001B[0m"

def welcome():
    print('Menu:')
    print('1. Add road')
    print('2. Delete road')
    print('3. Open system')
    print('0. Quit')

def add_road():
    global rotating_queue, counter
    road_name = input('Input road name: ')
    hold = 0
    if len(rotating_queue) < int(roads):
        if len(rotating_queue) != 0:
            position = circle.index(rotating_queue[0])
            hold = position
            if position == 0:
                rotating_queue.append(road_name)
            else:
                rotating_queue.insert(position, road_name)
        else:
            rotating_queue.append(road_name)
        circle.append(road_name)
        if len(circle) ==  1 or len(circle) == 2:
            timer.append(int(interval))
        else:
            if len(timer) == 0:
                timer.append((len(circle) - 1) * int(interval))
            else:
                h = circle.index(rotating_queue[0])
                index = timer[h]
                index = int(interval) - index
                timer.append((len(circle) - 1) * int(interval) - index)
                print('this got printed')
        if hold != 0:
            counter -= 1
            rotate()
        print(f'{road_name} added')
    else:
        print('Queue is Full')
    synchronise()
def delete_road():
    global circle, rotating_queue, timer, counter, decrement
    position = 0
    index = 0
    if len(rotating_queue) != 0:
        index = circle.index(rotating_queue[0])
        position = timer[index]
        for i in range(len(circle)):
            if circle[0] == rotating_queue[i]:
                circle.pop(0)
                timer.pop(i)
                print(f'{rotating_queue.pop(i)} deleted')
                break
        for p in range(len(timer)):
            if p == 0 or p == 1:
                timer[p] = position
            else:
                timer[p] = int(interval) * p - int(interval)
        counter -= 1
    else:
        print('Queue is empty')

    if len(rotating_queue) == 0:
        decrement = int(interval)
def traffic_lights():
    if len(rotating_queue) != 0:
        index = rotating_queue[0]
        for i in range(len(circle)):
            print(f"{circle[i]} will be {ANSI_GREEN + 'open' if index == circle[i] else ANSI_RED + 'closed'} for {timer[i]}s.{ANSI_RESET}")
def synchronise():
    if len(timer) == 2:
        t = timer[0]
        timer[1] = t
def count_down():
    for i in range(len(timer)):
        timer[i] -= 1
def rotate():
    global counter
    for c in range(counter):
        f = timer.pop(len(circle) - 1)
        timer.insert(0, f)
    counter += 1
def systems_road():
    global decrement, counter
    while not display_event.is_set():
        os.system('cls' if os.name == 'nt' else 'clear')
        # Clear screen output and reprint each of the 4 lines
        print(f'! {seconds}s have passed since system startup !')
        print(f'! Number of roads: {roads} !')
        print(f'! Interval: {interval} !')
        print()
        if decrement < 1:
            if len(circle) != 0:
                if counter > len(circle):
                    counter = 1
                t = rotating_queue.pop(0)
                rotating_queue.append(t)

                timer.clear()
                for j in range(len(circle)):
                    if j == 0 or j == 1:
                        timer.append(int(interval))
                    else:
                        timer.append(j * int(interval))
                # for c in range(counter):
                #     f = timer.pop(len(circle) - 1)
                #     timer.insert(0, f)
                # counter += 1
                rotate()
            decrement = int(interval)
        traffic_lights()
        count_down()
        decrement -= 1
        print()
        print(f'! Press "Enter" to open menu !')
        time.sleep(1)
        # Move cursor up by 4 lines to overwrite information in place
        #print("\033[4A", end='', flush=True)

def system(event):
   global seconds
   seconds = 0
   while not event.is_set():
       seconds += 1
       time.sleep(1)

def error_handling(num):
    while True:
        if not num.isdigit() or int(num) <= 0:
            num = input('Error! Incorrect Input. Try again: ')
        else:
            break
    return num

def menu():
    global roads, interval, decrement
    print('Welcome to the traffic management systems!')
    roads = error_handling(input('Input the number of roads: '))
    interval = error_handling(input('Input the interval: '))
    # os.system('cls' if os.name == 'nt' else 'clear')
    decrement = int(interval)
    q = Queue(int(roads))
    event = threading.Event()
    t = Thread(target=system, args=(event,), name='QueueThread')
    t.start()
    start = True
    while True:
        welcome()
        user_input = input()
        if user_input == '0':
            print('Bye!')
            start = False
            if not start:
                event.set()
                t.join()
            break
        elif user_input == '1':
            add_road()
            input()

        elif user_input == '2':
            delete_road()
            input()

        elif user_input == '3':
            # Enter System state
            display_event.clear()
            display_thread = Thread(target=systems_road)
            display_thread.start()
            input()
            display_event.set()  # Stop the display thread
            display_thread.join()
            #os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print('Incorrect option')
            input()
        #os.system('cls' if os.name == 'nt' else 'clear')
        
menu()
