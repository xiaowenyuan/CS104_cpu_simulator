# Codecademy CS104: Computer Architecture Portfolio Project

## Introduction

For ths portfolio project, Codecademy wants us to build a Python program that simulates the functions of a CPU. This project specifically simulates an ISA that handles MIPS instructions and can fetch and parse instructions to and from memory (main or cache) and the General Purpose Register (GPR).

As this program uses Pattern Matching, Python 3.10.0 (or later) is required to run it.

## Design

`script.py` contains simulation of the CPU's Control function, Program Counter (PC), main memory, GPR, and cache memory. 

### Main memory and cache memory

For simplification purposes, only 256 bytes of memory are simulated. The memory is word-aligned; hence, the memory label (which is in base 10) is in multiples of 4. If there are more than 64 data/instructions in the main memory, the program will terminate by way of an Exception as it would have run out of memory.

Cache can be turned on and off by way of MIPS instruction (`CACHE,1`). It is off by default. The size of the cache can be changed in the program itself when initialising the `Cache` object. By default, the size of the cache memory is 4 words. The design of the cache is fully associative (as the simulated main memory is very small to begin with), with a FIFO replacement policy as well as a Write-Back writing policy. The latter means that when there is an instruction to save into memory (`SW`), the memory address and the corresponding data are first saved in cache memory and will only be written into the main memory when the cache memory is about to be replaced.

### Instruction parsing

Instructions are to be uploaded by way of a `.txt` file placed in the same directory of `script.py`. Running `script.py` will prompt the user to type in the name of the `.txt` file containing the MIPS instructions. 

Upon uploading, each instruction is turned into an `Instruction` object. The method `instruction_breakdown` breaks down the string instruction into the corresponding OPCODE, destination register, constant, offsets, etc. 

The program runs by way of the `Control` function, which will run for as long as the PC still has valid memory address to point to (ie for the purpose of this simulation, the `Control` function will terminate once the PC value is over 252). 

The Control will check the memory address that the PC is pointing towards and fetch the data accordingly. It will then check if the data is a valid instruction (ie if it is an instance of `Instruction`). If it is a valid instruction, the OPCODE will determine the actions to be taken by way of pattern matching. Unless there is branching, jumping, or HALT instruction involved, the PC will then increment by 4 to point to the next memory address. 

The program will terminate once the PC has reached the end of the main memory address or if it encounters a `HALT` instruction.

## List of MIPS instructions simulated

Please note that valid instructions require the OPCODE and the different operand components to be separated by commas with NO spaces.

#### Arithmetic / Logical operations 
* ADD (`ADD,Rd,Rs,Rt`)
* ADDI (`ADDI,Rd,Rs,Const`)
* SUB (`SUB,Rd,Rs,Rt`)
* MULT (`MULT,Rd,Rs,Rt`)
* AND (`AND,Rd,Rs,Rt`)
* ANDI (`ANDI,Rd,Rs,Const`)
* OR (`OR,Rd,Rs,Rt`)
* ORI (`ORI,Rd,Rs,Const`)
* SLT (`SLT,Rd,Rs,Rt`)

#### Branching / Jumping
* J (`J,Address`)
* JAL (`JAL,Address`)
* JR (`JR,31`) Please note that **only 31** (ie only $ra / R31) is accepted as an operand for `JR`
* BNE (`BNE,Rs,Rt,Offset`)
* BEQ (`BNE,Rs,Rt,Offset`)

#### Data Transfer
* LW(`LW,Rd,Offset(Rs)`)
* SW(`SW,Rs,Offset(Rt)`))

#### Cache

* CACHE(`CACHE,1`) (or `CACHE,0` to turn it off--it is off by default)

#### Terminating program

* HALT(`HALT`)

## How to run this program

Run `script.py` and then type the `.txt` file name containing the instructions. Codecademy provided `instruction_input.txt` while I have also made a longer instructions file called `try_me.txt`. 

The Command Line Interface also takes in an optional argument `-d` or `--debug__print`. If the integer `0` is added as argument, the default debug print function will be turned off. The debug print is meant to provide an explanation into the working of the simulation. Without the debug print, `script.py` will only print out the resulting main memory, GPR, and cache memory.

Two test files called `test1.py` and `test2.py` can also be run to simulate more instructions--no external `.txt` file is required to run these as the registers and the main memory are already preprogrammed with some data. `test2.py` in particular gives a good overview of how the cache simulation works.

## Future improvements

* Add ability to switch to different Cache write policies (ie write-back vs write-through). 
