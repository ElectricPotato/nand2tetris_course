

from enum import Enum, auto

class CommandType(Enum):
    A_COMMAND = auto()
    C_COMMAND = auto()
    L_COMMAND = auto()


class Parser:
    def __init__(self, fileName) -> None:
        ''' Opens the input file/stream and gets ready to parse it.'''
        with open(fileName, 'r') as f:
            self.fileContents = f.readlines()

        self.currentCommandType = None
        self.currentSymbol = None

        self.currentDest = None
        self.currentComp = None
        self.currentJump = None

        self.currentLine = 0
        self.moreCommands = True

    def hasMoreCommands(self) -> bool:
        ''' Are there more commands in the input?'''
        return self.moreCommands

    def advance(self) -> None:
        '''Reads the next command from the input and makes it the current command.
           Should be called only if hasMoreCommands() is true.
           Initially there is no current command.'''
        
        self.currentCommandType = None
        self.currentSymbol = None

        self.currentDest = None
        self.currentComp = None
        self.currentJump = None
        
        while(True):
            if(self.currentLine >= len(self.fileContents)):
                self.moreCommands = False
                break
                
            line = self.fileContents[self.currentLine]
            line = line[:line.find('//')].strip() #remove comments
            foundCommand = False
            if(line != ""):
                if(line[0] == '@'):
                    self.currentCommandType = CommandType.A_COMMAND
                    self.currentSymbol = line[1:]
                    foundCommand = True
                elif(line[0] == '('):
                    self.currentCommandType = CommandType.L_COMMAND
                    self.currentSymbol = line[1:-1]
                    foundCommand = True
                else:
                    self.currentCommandType = CommandType.C_COMMAND

                    if(";" in line):
                        line, self.currentJump = line.split(";")
                    else:
                        self.currentJump = ''

                    if("=" in line):
                        self.currentDest, line = line.split("=")
                    else:
                        self.currentDest = ''

                    self.currentComp = line
                    foundCommand = True

            self.currentLine += 1
            if(foundCommand):
                break

        return

    def returnToStart(self) -> None:
        '''Goes back to the beggining of the file to start parsing it from the start'''
        self.currentLine = 0

        self.currentCommandType = None
        self.currentSymbol = None

        self.currentDest = None
        self.currentComp = None
        self.currentJump = None

        self.moreCommands = True

    def commandType(self) -> CommandType:
        '''Returns the type of the current command:
            - A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
            - C_COMMAND for "dest=comp;jump"
            - L_COMMAND (actually, pseudocommand) for (Xxx) where Xxx is a symbol.'''
        return self.currentCommandType
    
    def symbol(self) -> str:
        '''Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx).
        Should be called only when commandType() is A_COMMAND or L_COMMAND.'''
        return self.currentSymbol

    def dest(self) -> str:
        '''Returns the dest mnemonic in the current C-command (8 possibilities).
        Should be called only when commandType() is C_COMMAND.'''
        return self.currentDest

    def comp(self) -> str:
        '''Returns the comp mnemonic in the current C-command (28 possibilities).
        Should be called only when commandType() is C_COMMAND.'''
        return self.currentComp

    def jump(self) -> str:
        '''Returns the jump mnemonic in the current C-command (8 possibilities).
        Should be called only when commandType() is C_COMMAND.'''
        return self.currentJump

class CodeGen:
    def dest(mnemonic: str) -> str:
        #Returns the binary code of the dest mnemonic (3 bits).
        #ADM
        return ''.join([str(int(i in mnemonic)) for i in 'ADM'])
        
    def comp(mnemonic: str) -> str:
        #Returns the binary code of the comp mnemonic (7 bits).

        mnemonicTable = {
            '0'  : "0101010",
            '1'  : "0111111",
            '-1' : "0111010",
            'D'  : "0001100",
            'A'  : "0110000",
            '!D' : "0001101",
            '!A' : "0110001",
            '-D' : "0001111",
            '-A' : "0110011",
            'D+1': "0011111",
            'A+1': "0110111",
            'D-1': "0001110",
            'A-1': "0110010",
            'D+A': "0000010",
            'D-A': "0010011",
            'A-D': "0000111",
            'D&A': "0000000",
            'D|A': "0010101",
            'M'  : "1110000",
            '!M' : "1110001",
            '-M' : "1110011",
            'M+1': "1110111",
            'M-1': "1110010",
            'D+M': "1000010",
            'D-M': "1010011",
            'M-D': "1000111",
            'D&M': "1000000",
            'D|M': "1010101"
        }

        return mnemonicTable[mnemonic]
        
    def jump(mnemonic: str) -> str:
        #Returns the binary code of the jump mnemonic (3 bits).
        '''
            Conditional jump logic
            0 0 0 null No jump         | 0
            0 0 1 JGT If out >  0 jump | !(zr | ng)
            0 1 0 JEQ If out =  0 jump | zr
            0 1 1 JGE If out >= 0 jump | !ng
            1 0 0 JLT If out <  0 jump | ng
            1 0 1 JNE If out != 0 jump | !zr
            1 1 0 JLE If out <= 0 jump | zr | ng
            1 1 1 JMP Jump             | 1
        '''

        if  (mnemonic == ''   ):return '000'
        elif(mnemonic == 'JGT'):return '001'
        elif(mnemonic == 'JEQ'):return '010'
        elif(mnemonic == 'JGE'):return '011'
        elif(mnemonic == 'JLT'):return '100'
        elif(mnemonic == 'JNE'):return '101'
        elif(mnemonic == 'JLE'):return '110'
        elif(mnemonic == 'JMP'):return '111'
        
class SymbolTable:
    def __init__(self) -> None:
        #Creates a new empty symbol table.
        self.table = {
            "SP"        : 0x0000,
            "LCL"       : 0x0001,
            "ARG"       : 0x0002,
            "THIS"      : 0x0003,
            "THAT"      : 0x0004,
            "SCREEN"    : 0x4000,
            "KBD"       : 0x6000,
        }
        self.table.update({f"R{i}": i for i in range(16)}) #add R0-R15 mnemonics

    def addEntry(self, symbol: str, address: int):
        #Adds the pair (symbol, address) to the table.
        self.table[symbol] = address

    def contains(self, symbol: str) -> bool:
        #Does the symbol table contain the given symbol?
        return symbol in self.table
    
    def GetAddress(self, symbol: str) -> int:
        #Returns the address associated with the symbol.
        return self.table[symbol]

def assemble(inputFileName, outputFileName):
    p = Parser(inputFileName)
    p.advance() #advance to first symbol

    symbolTable = SymbolTable()

    #1st pass - populate the symbol table

    baseAddress = 0x1000 #TODO
    currentAddress = baseAddress
    while(p.hasMoreCommands()):  #TODO: this needs fixed
        commandType = p.commandType()
        if(commandType == CommandType.L_COMMAND):
            if(not p.symbol().isdecimal() and not symbolTable.contains(p.symbol())):
                symbolTable.addEntry(p.symbol(), currentAddress)
                currentAddress += 1

        p.advance()


    #2nd pass
    p.returnToStart()
    p.advance() #advance to first symbol

    machineCode = []

    while(p.hasMoreCommands()):
        if(p.commandType() == CommandType.A_COMMAND):
            if(not p.symbol().isdecimal()):
                #look up symbol in the table to get an address
                if(not symbolTable.contains(p.symbol())):
                    raise Exception(f"Second pass found a symbol that the first pass missed: {p.symbol()}")

                address = symbolTable.GetAddress(p.symbol())
            else:
                #interpret as decimal integer
                address = int(p.symbol())

            if(address > 0x7FFF): raise Exception("address too big to encode")
            machineInstruction = f'0{address:>015b}' #format address as 15

        elif(p.commandType() == CommandType.C_COMMAND):
            machineInstruction = \
                '111' \
                + CodeGen.dest(p.dest()) \
                + CodeGen.comp(p.comp()) \
                + CodeGen.jump(p.jump())

        assert(len(machineInstruction) == 16)
        machineCode.append(machineInstruction)

        p.advance()

    with open(outputFileName, 'w') as f:
        for line in machineCode:
            f.write(line + "\n")


import os


    #programs with symbols

if(__name__ == "__main__"):
    #Symbol-less assembly programs
    inputFileNames = [
        #"../add/Add.asm",
        #"../max/MaxL.asm",
        #"../pong/PongL.asm",
        #"../rect/RectL.asm",
        #"../max/Max.asm",
        #"../pong/Pong.asm",
        "../rect/Rect.asm"
    ]


    for inputFileName in inputFileNames:
        inputFilePath = os.path.realpath(os.path.join(os.path.dirname(__file__), inputFileName))
        outputFilePath = inputFilePath + ".o"

        assemble(inputFilePath, outputFilePath)