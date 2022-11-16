// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the KBD input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

//loop:
//  M[R0]=-1
//  R0+=1
//  if R0-1000 != 0 goto loop

(mainLoop)
    (KBLoop1)
        @KBD
        D=M
        @KBLoop1
        D;JEQ //while(M[KBD] == 0){}

        @SCREEN
        M=-1 //M[SCREEN]=0xFFFF
        D=A
        @R0
        M=D     //R0 = SCREEN
    (FillLoop1)
        @R0
        AMD=M+1 //R0+=1
        M=-1    //M[R0]=0xFFFF
        @16394  //END of screen buffer, shortened for testing in emulator: 16384+10
        D=D-A
        @FillLoop1
        D;JNE  //if R0 != 100 goto FillLoop1

    (KBLoop2)
        @KBD
        D=M
        @KBLoop2
        D;JNE    //while(M[KBD] != 0){}

        @SCREEN
        M=0 //M[SCREEN]=0
        D=A
        @R0
        M=D     //R0 = SCREEN
    (FillLoop2)
        @R0
        AMD=M+1 //R0+=1
        M=0     //M[R0]=0
        @16394  //END of screen buffer, shortened for testing in emulator
        D=D-A
        @FillLoop2
        D;JNE  //if R0 != 100 goto FillLoop2

    @mainLoop
    0;JMP


/////////////////////
//    @SCREEN
//(FillLoop)
//    M=-1
//    D=A
//    @100
//    D=D-A
//    @endFill
//    D;JGT
//    @101
//    D=D+A
//    @FillLoop
//    0;JMP
//(endFill)
//
//
///////////////////////
//(FillLoop)
//    @R0
//    AD=M
//    M=-1
//    @R0
//    M=D+1
//    @R1
//    MD=M-1
//    @FillLoop
//    D;JGT
//
///////////////////////
//(FillLoop)
//    @R0
//    AMD=M+1
//    M=-1
//    @100
//    D=D-A
//    @FillLoop
//    D;JGT
//
//
///////////////////////
//(FillLoop)
//    @R0
//    AM=M+1
//    M=-1
//    @R1
//    MD=M-1
//    @FillLoop
//    D;JGT