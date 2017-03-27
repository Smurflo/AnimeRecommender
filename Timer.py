import time

start_time = 0

def start():
    global start_time
    start_time = time.time()

def end(label="Time"):
    total_time = time.time() - start_time
    print(label + ": " + str(total_time) + " seconds")