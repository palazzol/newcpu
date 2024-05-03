// Move pixel around using arrow keys
// Select to quit

        LDI r1 15    // x
        LDI r2 15    // y

.loop   LDI r15 255     // Controller Input
        LOD r3 r15
      
        LDI r4 1        // Left
        AND r5 r4 r3
        CMP r5 r0
        BRH zero .nleft
        DEC r1 r1

.nleft  LDI r4 2        // Down
        AND r5 r4 r3
        CMP r5 r0
        BRH zero .ndown
        DEC r2 r2

.ndown  LDI r4 4        // Right
        AND r5 r4 r3
        CMP r5 r0
        BRH zero .nright
        INC r1 r1

.nright LDI r4 8        // Up
        AND r5 r4 r3
        CMP r5 r0
        BRH zero .nup
        INC r2 r2

.nup    LDI r4 16       // Select
        AND r5 r4 r3
        CMP r5 r0
        BRH zero .nsel
        HLT

.nsel   LDI r15 243     // clear old pixel
        STR r0 r15
        LDI r15 240     // new pixel x
        STR r1 r15
        LDI r15 241     // new pixel y
        STR r2 r15
        LDI r15 242     // draw pixel
        STR r0 r15
        LDI r15 245     // buffer screen
        STR r0 r15    
        JMP .loop
