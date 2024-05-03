// fill the screen with a double for loop
        LDI r1 32
.x_loop CMP r1 r0 
        BRH zero .x_done
        DEC r1

        LDI r2 32
.y_loop CMP r2 r0
        BRH zero .y_done
        DEC r2
        
        LDI r15 240     // pixel x
        STR r1 r15
        LDI r15 241     // pixel y
        STR r2 r15
        LDI r15 242     // draw pixel
        STR r0 r15      
        
        JMP .y_loop

.y_done JMP .x_loop
.x_done LDI r15 245     // buffer screen
        STR r0 r15
        HLT
