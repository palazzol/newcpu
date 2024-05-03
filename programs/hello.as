// Hello World!

LDI r15 249     // clear character display
STR r0 r15
LDI r15 247     // write character
LDI r1 "H"
STR r1 r15
LDI r1 "e"
STR r1 r15
LDI r1 "l"
STR r1 r15
LDI r1 "l"
STR r1 r15
LDI r1 "o"
STR r1 r15
LDI r1 " "
STR r1 r15
LDI r1 "W"
STR r1 r15
LDI r1 "o"
STR r1 r15
LDI r1 "r"
STR r1 r15
LDI r1 "l"
STR r1 r15
LDI r1 "d"
STR r1 r15
LDI r1 "!"
STR r1 r15
LDI r15 258     // push buffer
STR r0 r15
HLT
