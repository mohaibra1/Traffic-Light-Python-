import threading, os
from itertools import count
from threading import Thread
import time
from queue import Queue

seconds = 0
# Events to control thread behavior
system_event = threading.Event()
display_event = threading.Event()
roads = 0
interval = 0
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

def add_road(q, road):
    road_name = input('Input road name: ')
    if not q.full():
        q.put(road_name)
        print(f'{road_name} added')
    else:
        print('Queue is Full')
def delete_road(q, road):
    if not q.empty():
        print(f'{q.get()} deleted')
    else:
        print('Queue is empty')
def systems_road(q):
    count_down = int(interval)
    temp = []
    for i in q.queue:
       temp.append(i)
    while not display_event.is_set():
        if count_down < 1:
            count_down = int(interval)
        os.system('cls' if os.name == 'nt' else 'clear')
        # Clear screen output and reprint each of the 4 lines
        print(f'! {seconds}s have passed since system startup !')
        print(f'! Number of roads: {roads} !')
        print(f'! Interval: {interval} !')
        print()
        if len(temp) == 1:
            print(f'Road "{temp[0]}" will be open for {count_down}s.')
        else:
            for j in range(len(temp)):
                if j == 0:
                    print(f'Road "{temp[j]}" will be open for {count_down }s.')
                elif j == 1:
                    print(f'Road "{temp[j]}" will be closed for {count_down}s.')
                else:
                    s = (count_down * j) - 1
                    print(f'Road "{temp[j]}" will be closed for {s}s.')
        print()
        print(f'! Press "Enter" to open menu !')
        count_down -= 1
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
    global roads, interval
    print('Welcome to the traffic management systems!')
    roads = error_handling(input('Input the number of roads: '))
    interval = error_handling(input('Input the interval: '))
    # os.system('cls' if os.name == 'nt' else 'clear')
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
            add_road(q, user_input)
            input()

        elif user_input == '2':
            delete_road(q, user_input)
            input()

        elif user_input == '3':
            # Enter System state
            display_event.clear()
            display_thread = Thread(target=systems_road, args=(q,))
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
