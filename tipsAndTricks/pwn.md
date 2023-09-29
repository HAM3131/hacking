# Overview
Pwn is a categegory of challenges focused on binary exploitation: exploiting poorly implemented functions to arbitrarily write or read in the server until you can extract the target information. One of the most common such vulnerabilities is a `buffer overflow`, but there are other vulnerabilities like the `format string bug`. Sometimes the solution will be as simple as to overwrite another variable to what you want, and other times the object is to use `return oriented programming` to alter the control flow of the program.

# Buffer Overflow

# Format String Bug
The format string vulnerability exists in `C/C++` when the implementation uses a function like `printf()` to print user input. Because the function includes format string functionality, a user can use format specifiers in their input to arbitrarily read or right on the host.
```{C++} 
#include <stdio.h>

int secret = 0;

int main() {
    char input[100];

    puts("input: ");
    fgets(input, sizeof input, stdin);
    
    // SAFE USAGE OF PRINTF()
    printf("%s", input);
    // UNSAFE USAGE OF PRINTF()
    printf(input);
}
```
When a format specifier requires a variable to be passed to the function to operate, it looks on the stack. This means that when there is user input (like above) and the format string vulnerability is present, the user can actuall write the values of the variables they are referencing too! The format specifiers will look to the stack, and find the input buffer there. There might be some space between the start of the input buffer and the end of the stack though, so you can use `#$` as a flag for the format specifier to indicate which argument `#` to look to. Then, if the buffer is 6 longs from the end of the stack and you want to read start of the string, you could use `%6$x`.

# Return Oriented Programmeing