//R2=0
//for i in range(R1):
//    R2+=R0
//
//----
//R2=0
//loop:
//    if R1 == 0 goto end;
//    R1 -= 1;
//    R2 += R0
//    goto loop;
//end:

    @R2 //R2=0
    M=0

(loop)
    @R1
    D=M
    @end
    D;JEQ  //if R1 == 0 goto end;

    @R1    //R1 -= 1;
    MD=M-1

    @R0    //R2 += R0;
    D=M
    @R2
    M=M+D

    @loop
    0;JMP  //goto loop    //longer loop - 12 inst per loop
(end)
    @end
    0;JMP