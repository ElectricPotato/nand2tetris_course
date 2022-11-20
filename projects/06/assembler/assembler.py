

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

    def hasMoreCommands(self) -> bool:
        ''' Are there more commands in the input?'''
        return True

    def advance(self) -> None:
        '''Reads the next command from the input and makes it the current command.
           Should be called only if hasMoreCommands() is true.
           Initially there is no current command.'''
        return

    def commandType(self) -> CommandType:
        '''Returns the type of the current command:
            - A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
            - C_COMMAND for "dest=comp;jump"
            - L_COMMAND (actually, pseudocommand) for (Xxx) where Xxx is a symbol.'''
        return CommandType.A_COMMAND
    
    def symbol(self) -> str:
        '''Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx).
        Should be called only when commandType() is A_COMMAND or L_COMMAND.'''
        return ''

    def dest(self) -> str:
        '''Returns the dest mnemonic in the current C-command (8 possibilities).
        Should be called only when commandType() is C_COMMAND.'''
        return ''

    def comp(self) -> str:
        '''Returns the comp mnemonic in the current C-command (28 possibilities).
        Should be called only when commandType() is C_COMMAND.'''
        return ''

    def jump(self) -> str:
        '''Returns the jump mnemonic in the current C-command (8 possibilities).
        Should be called only when commandType() is C_COMMAND.'''
        return ''

class CodeGen:
    def dest(mnemonic: str) -> str:
        #Returns the binary code of the dest mnemonic (3 bits).
        return ''
        
    def comp(mnemonic: str) -> str:
        #Returns the binary code of the comp mnemonic (7 bits).
        return ''
        
    def jump(mnemonic: str) -> str:
        #Returns the binary code of the jump mnemonic (3 bits).
        return ''
        
class SymbolTable:
    def __init__(self) -> None:
        #Creates a new empty symbol table.
        pass

    def addEntry(symbol: str, address: int):
        #Adds the pair (symbol, address) to the table.
        return

    def contains(symbol: str) -> bool:
        #Does the symbol table contain the given symbol?
        return False
    
    def GetAddress(symbol: str) -> int:
        #Returns the address associated with the symbol.
        return 0

#Symbol-less assembly programs
inputFileName = "../add/Add.asm"
#inputFileName = "../max/MaxL.asm"
#inputFileName = "../pong/PongL.asm"
#inputFileName = "../rect/RectL.asm"

#programs with symbols
#inputFileName = "../max/Max.asm"
#inputFileName = "../pong/Pong.asm"
#inputFileName = "../rect/Rect.asm"


p = Parser(inputFileName)
symbolTable = SymbolTable()

while(p.hasMoreCommands()):
    p.advance()