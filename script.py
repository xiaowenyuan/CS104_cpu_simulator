import argparse 

is_debug = True 
def debugprint(s):
    if is_debug == True: 
        print(s)
# Make a memory class, which will hold instructions as well as data that cannot fit into the general purpose registers
class Memory: 
    def __init__(self):
        # For the purposes of this simulation, the memory will only have 256 addresses.
        # The addresses are in base 10 instead of base 16. We also assume that each address is word-based (stores 4 bytes instead of 1). The addresses are therefore in multiples of 4.
        self.memory_addresses = {}
        debugprint('\nMemory is initialised.')
        for i in range(0, 256,4): 
            self.memory_addresses[i] = None
            debugprint(f'Memory address {i} is initialised with an initial value of {self.memory_addresses[i]}')
        self.cache_active = False
    
    def store_into_memory(self, address, value_to_store):
        self.memory_addresses[address] = value_to_store 
        debugprint(f'\nStoring {value_to_store} in memory address {address}')
    
    def load_from_memory(self, address):
        debugprint(f'\nLoading {self.memory_addresses[address]} from memory address {address}')
        return self.memory_addresses[address]
    
    def print_memory(self):
        print(f'\n\n\n----------Printing memory----------')
        for key,value in self.memory_addresses.items():
            print(f'{key}: {value}')
        
    # This method selects a free memory in which data or instructions can be stored.
    # Assumption: for every simulation run, the 256 memory addresses cannot be exhausted. 
    def select_available_memory(self):
        selected_memory = None
        for i in range (0, 256, 4):
            if self.memory_addresses[i] == None:
                selected_memory = i
                break
            else:
                continue
        if selected_memory == None:
            raise Exception('\nRan out of memory!')
        return selected_memory 

    # Memory class has method to load from file instructions that will be stored in available memory
    def load_instructions_into_memory(self, file):
        instructions_list = []
        with open(file) as instruction_file: 
            instructions_list += instruction_file.readlines()
        for instruction in instructions_list:
            selected_memory = self.select_available_memory()
            instruction_object = Instruction(instruction)
            self.store_into_memory(selected_memory, instruction_object)
        print('\nInstructions are successfully loaded into memory.')

class CacheEntry:
    def __init__(self, tag, data):
        self.tag = tag
        self.data = data

    def __repr__(self):
        return f'{self.tag} : {self.data}'

class Cache:
    def __init__(self, cache_size = 4):
        self.cache_bank = []
        self.cache_size = cache_size
        debugprint(f'\nCache of size {self.cache_size} is initialised.')
        self.fifo_index = 0 
        
    def store_into_cache(self, address, value_to_store, main_memory):
        # check if memory address already exists as a tag in cache
        for cache_entry in self.cache_bank:
            if cache_entry.tag == address:
                debugprint(f'\nMemory address {address} already exists in cache. The cache for memory address {address} will be updated with the data {value_to_store}.')
                cache_entry.data = value_to_store
                return
        if len(self.cache_bank) + 1 > self.cache_size:
            debugprint(f'\nAs cache size {self.cache_size} is reached, replacement policy will be implemented.')
            self.replace_entry(address, value_to_store, main_memory)
        else: 
            self.cache_bank.append(CacheEntry(address, value_to_store))
        debugprint(f'\nMemory address {address} with data {value_to_store} is cached.')
    
    def replace_entry(self, address, value_to_store, main_memory):
        cache_entry = self.cache_bank[self.fifo_index]
        # Write the cache data into main memory before it's replaced
        debugprint(f'\nWriting cache data {cache_entry.data} into main memory address {cache_entry.tag} prior to replacement.')
        main_memory.store_into_memory(cache_entry.tag, cache_entry.data)
        cache_entry.tag = address
        cache_entry.data = value_to_store
        debugprint(f'\nCache data has been replaced with {cache_entry.tag} : {cache_entry.data}')
        self.fifo_index += 1 
        debugprint(f'\nCache FIFO index is now {self.fifo_index}')
        if self.fifo_index >= self.cache_size: 
            self.fifo_index = 0 
            debugprint(f'\nCache FIFO index is restarted to 0')

    def load_from_cache(self, address):
        for cache_entry in self.cache_bank:
            if cache_entry.tag == address:
                debugprint(f'\nCache hit for memory address {address}!')
                return cache_entry.data
        debugprint(f'\nCache miss for memory address {address}!')
        return None
    
    def print_cache(self):
        print(f'\n\n\n----------Printing cache----------')
        for cache_entry in self.cache_bank:
            print(cache_entry)

        
# Instruction class--each line of instruction is turned into an instruction object 
class Instruction:
    def __init__(self, instruction_str):
        self.instruction_str = instruction_str
        self.opcode = None 
        self.rd = None
        self.rs = None
        self.rt = None
        self.constant = None
        self.offset = None
        self.address = None
        self.cache_bool = None
        self.instruction_breakdown(instruction_str)
    def __repr__(self):
        stripped_instruction_str = self.instruction_str.strip('\n')
        return stripped_instruction_str
    #Instruction class has method that breaks down instructions into opcodes and operands depending on the opcodes 
    def instruction_breakdown(self, instruction_str):
        instruction_list = instruction_str.split(',')
        operations_list = ['ADD', 'SUB', 'MULT', 'AND', 'OR', 'SLT']
        operations_constant_list = ['ADDI', 'ANDI', 'ORI']
        jumps_list = ['J', 'JAL']
        self.opcode = instruction_list[0]
        for i in range(1, len(instruction_list)):
            instruction_list[i] = instruction_list[i].strip('rR$\n')
        if self.opcode in operations_list:
            if len(instruction_list) != 4:
                raise ValueError('Invalid instruction length.')
            try:
                self.rd = int(instruction_list[1])
                self.rs = int(instruction_list[2])
                self.rt = int(instruction_list[3])
            except:
                raise ValueError(f'Inappropriate instruction format following OPCODE; should be an integer.')
        elif self.opcode in operations_constant_list:
            if len(instruction_list) != 4:
                raise ValueError('Invalid instruction length.')
            try:
                self.rd = int(instruction_list[1])
                self.rs = int(instruction_list[2])
                self.constant = int(instruction_list[3])
            except:
                raise ValueError(f'Inappropriate instruction format following OPCODE; should be an integer.')
        elif self.opcode in jumps_list:
            if len(instruction_list) != 2:
                raise ValueError('Invalid instruction length.')
            try:
                self.address = int(instruction_list[-1])
            except:
                raise ValueError(f'Inappropriate instruction format following OPCODE; should be an integer.')
        elif self.opcode == 'JR':
            if len(instruction_list) != 2:
                raise ValueError('Invalid instruction length.')
            try:
                self.address = int(instruction_list[-1])
            except:
                raise ValueError(f'Inappropriate instruction format following OPCODE; should be an integer.')
            if self.address != 31: 
                raise ValueError('Invalid register address. JR OPCODE should operate on $ra (R31).')
        elif self.opcode == 'BNE' or self.opcode =='BEQ':
            if len(instruction_list) != 4:
                raise ValueError('Invalid instruction length.')
            try:
                self.rs = int(instruction_list[1])
                self.rt = int(instruction_list[2])
                self.offset = int(instruction_list[3])
            except:
                raise ValueError(f'Inappropriate instruction format following OPCODE; should be an integer.')
        elif self.opcode == 'LW':
            if len(instruction_list) != 3:
                raise ValueError('Invalid instruction length.')
            try:
                self.rd = int(instruction_list[1])
                if '(' in instruction_list[-1]:
                    memory_instruction_list = instruction_list[-1].split('(')
                    debugprint(memory_instruction_list)
                    memory_instruction_list_stripped = memory_instruction_list[-1].strip('()')
                    self.offset = int(memory_instruction_list[0])
                    self.rs = int(memory_instruction_list_stripped)
                else:
                    self.rs = int(instruction_list[-1])
            except:
                raise ValueError(f'Inappropriate instruction format following OPCODE; should be an integer.')
        elif self.opcode == 'SW':
            if len(instruction_list) != 3:
                raise ValueError('Invalid instruction length.')
            try:
                self.rs = int(instruction_list[1])
                if '(' in instruction_list[-1]:
                    memory_instruction_list = instruction_list[-1].split('(')
                    memory_instruction_list_stripped = memory_instruction_list[-1].strip('()')
                    self.offset = int(memory_instruction_list[0])
                    self.rt = int(memory_instruction_list_stripped)
                else:
                    self.rt = int(instruction_list[-1])
            except:
                raise ValueError(f'Inappropriate instruction format following OPCODE; should be an integer.')
        elif self.opcode == 'CACHE':
            if len(instruction_list) != 2:
                raise ValueError('Invalid instruction length.')
            self.cache_bool = int(instruction_list[-1])
        elif self.opcode =='HALT':
            if len(instruction_list) > 2:
                raise ValueError('Invalid instruction length.') 
        else: 
            raise ValueError('Inappropriate OPCODE')

# Make a general purpose register class, which holds 32 registers (0 - 31).

class GPR:
    def __init__(self):
        debugprint(f'\nThe GPR has been initialised.')
        self.register = {}
        for i in range(0, 32): 
            self.register[i] = 0
            debugprint(f'\nRegister {i} is initialised with a value of {self.register[i]}.')
        self.store_into_GPR(0, 0)
    
    # Make a method to store into register
    def store_into_GPR(self, address, value):
        self.register[address] = value
        debugprint(f'\nThe data {value} is stored in register {address}.')

    # Make a method to load data from register
    def load_from_GPR(self, address):
        data_loaded = self.register[address]
        debugprint(f'\nFetching data {data_loaded} from register {address}')
        return data_loaded

    # Method to print out all the data in the register
    def print_register(self):
        print('\n\n\n----------Printing register----------')
        for entry in self.register:
            print(f'{entry} : {self.register[entry]}')

# Define Program Counter (PC)

class Program_Counter:
    def __init__(self):
        self.value = 0
        debugprint(f'\nThe PC has been initialised with a value of {self.value}')
    
    def jump_count(self, new_value):
        self.value = new_value
        debugprint(f'\nThe PC\'s value is now {self.value}')
    
    def increment_count(self, increment_value):
        self.value += increment_value 
        debugprint(f'\nThe PC\'s value is now {self.value}')
    
    def see_count(self):
        return self.value

def control(program_counter, memory, cache, gpr):
    stop_count = len(memory.memory_addresses)*4 - 4
    while program_counter.see_count() <= stop_count:
        # The instruction register will fetch data in the memory that the PC is pointing at
        debugprint(f'\n\n\n\nThe PC points at memory address {program_counter.see_count()} and will fetch the data stored therein.')
        fetched_data = memory.load_from_memory(program_counter.see_count())
        # Check if fetched_data is valid instruction
        if isinstance(fetched_data, Instruction):
            fetched_instruction = fetched_data
            debugprint(f'\nThe fetched data from memory address {program_counter.see_count()} is a valid instruction {fetched_instruction}')
            # The control decodes the fetched instruction and decides what to do
            # Check for the opcode of the instruction 
            instruction_opcode = fetched_instruction.opcode 
            debugprint(f'\nThe control will perform {instruction_opcode} based on the instruction {fetched_instruction}')
            # The control will perform the appropriate operation depending on the opcode 
            match instruction_opcode:
                case 'ADD': 
                    # Fetch the data in Rs and Rt 
                    rs_data = gpr.load_from_GPR(fetched_instruction.rs)
                    debugprint(f'\n{rs_data} has been fetched from register {fetched_instruction.rs}')
                    rt_data = gpr.load_from_GPR(fetched_instruction.rt)
                    debugprint(f'\n{rt_data} has been fetched from register {fetched_instruction.rt}')
                    # Perform the addition operation 
                    result = rs_data + rt_data
                    debugprint(f'\n{rt_data} + {rs_data} = {result}')
                    # Store the result in the specified Rd address
                    gpr.store_into_GPR(fetched_instruction.rd, result)
                    debugprint(f'\n{result} is now stored in register {fetched_instruction.rd}')
                    program_counter.increment_count(4)
                case 'SUB':
                    # Fetch the data in Rs and Rt 
                    rs_data = gpr.load_from_GPR(fetched_instruction.rs)
                    debugprint(f'\n{rs_data} has been fetched from register {fetched_instruction.rs}')
                    rt_data = gpr.load_from_GPR(fetched_instruction.rt)
                    debugprint(f'\n{rt_data} has been fetched from register {fetched_instruction.rt}')
                    # Perform the subtraction operation 
                    result = rs_data - rt_data 
                    debugprint(f'\n{rs_data} - {rt_data} = {result}')
                    # Store the result in the specified Rd address
                    gpr.store_into_GPR(fetched_instruction.rd, result)
                    debugprint(f'\n{result} is now stored in register {fetched_instruction.rd}')
                    program_counter.increment_count(4)
                case 'MULT':
                    # Fetch the data in Rs and Rt 
                    rs_data = gpr.load_from_GPR(fetched_instruction.rs)
                    debugprint(f'\n{rs_data} has been fetched from register {fetched_instruction.rs}')
                    rt_data = gpr.load_from_GPR(fetched_instruction.rt)
                    debugprint(f'\n{rt_data} has been fetched from register {fetched_instruction.rt}')
                    # Perform the multiplication operation 
                    result = rs_data * rt_data 
                    debugprint(f'\n{rt_data} * {rs_data} = {result}')
                    # Store the result in the specified Rd address
                    gpr.store_into_GPR(fetched_instruction.rd, result)
                    debugprint(f'\n{result} is now stored in register {fetched_instruction.rd}')
                    program_counter.increment_count(4)
                case 'AND':
                    # Fetch the data in Rs and Rt 
                    rs_data = gpr.load_from_GPR(fetched_instruction.rs)
                    debugprint(f'\n{rs_data} has been fetched from register {fetched_instruction.rs}')
                    rt_data = gpr.load_from_GPR(fetched_instruction.rt)
                    debugprint(f'\n{rt_data} has been fetched from register {fetched_instruction.rt}')
                    # Perform the bitwise AND operation
                    result = rs_data & rt_data 
                    debugprint(f'\n{rt_data} AND {rs_data} = {result}')
                    # Store the result in the specified Rd address
                    gpr.store_into_GPR(fetched_instruction.rd, result)
                    debugprint(f'\n{result} is now stored in register {fetched_instruction.rd}')
                    program_counter.increment_count(4)
                case 'OR':
                    # Fetch the data in Rs and Rt 
                    rs_data = gpr.load_from_GPR(fetched_instruction.rs)
                    debugprint(f'\n{rs_data} has been fetched from register {fetched_instruction.rs}')
                    rt_data = gpr.load_from_GPR(fetched_instruction.rt)
                    debugprint(f'\n{rt_data} has been fetched from register {fetched_instruction.rt}')
                    # Perform the bitwise OR operation
                    result = rs_data | rt_data 
                    debugprint(f'\n{rt_data} OR {rs_data} = {result}')
                    # Store the result in the specified Rd address
                    gpr.store_into_GPR(fetched_instruction.rd, result)
                    debugprint(f'\n{result} is now stored in register {fetched_instruction.rd}')
                    program_counter.increment_count(4)
                case 'SLT':
                    # Fetch the data in Rs and Rt 
                    rs_data = gpr.load_from_GPR(fetched_instruction.rs)
                    debugprint(f'\n{rs_data} has been fetched from register {fetched_instruction.rs}')
                    rt_data = gpr.load_from_GPR(fetched_instruction.rt)
                    debugprint(f'\n{rt_data} has been fetched from register {fetched_instruction.rt}')
                    # If Rs < Rt, store 1 in Rd, otherwise store 0 in Rd
                    if rs_data < rt_data:
                        debugprint(f'\n{rs_data} is less than {rt_data}.')
                        gpr.store_into_GPR(fetched_instruction.rd, 1)
                        debugprint(f'\n1 is now stored in register {fetched_instruction.rd}')
                    else:
                        debugprint(f'\n{rs_data} is NOT less than {rt_data}.')
                        gpr.store_into_GPR(fetched_instruction.rd, 0)
                        debugprint(f'\n0 is now stored in register {fetched_instruction.rd}')
                    program_counter.increment_count(4)
                case 'BNE':
                    # Fetch the data in Rs and Rt 
                    rs_data = gpr.load_from_GPR(fetched_instruction.rs)
                    debugprint(f'\n{rs_data} has been fetched from register {fetched_instruction.rs}')
                    rt_data = gpr.load_from_GPR(fetched_instruction.rt)
                    debugprint(f'\n{rt_data} has been fetched from register {fetched_instruction.rt}')
                    offset_data = fetched_instruction.offset
                    debugprint(f'\nThe offset figure {offset_data} has been fetched from register {fetched_instruction.offset}')
                    # If Rs != Rt, PC += (4 + offset * 4)
                    if rs_data != rt_data:
                        pc_increment = 4 + (offset_data * 4)
                        debugprint(f'\n{rs_data} != {rt_data}. The PC will be incremented by {pc_increment}')
                        program_counter.increment_count(pc_increment)
                    else:
                        debugprint(f'\n{rs_data} == {rt_data}. No branching is done.')
                        program_counter.increment_count(4)
                case 'BEQ':
                    # Fetch the data in Rs and Rt 
                    rs_data = gpr.load_from_GPR(fetched_instruction.rs)
                    debugprint(f'\n{rs_data} has been fetched from register {fetched_instruction.rs}')
                    rt_data = gpr.load_from_GPR(fetched_instruction.rt)
                    debugprint(f'\n{rt_data} has been fetched from register {fetched_instruction.rt}')
                    offset_data = fetched_instruction.offset
                    debugprint(f'\nThe offset figure {offset_data} has been fetched from register {fetched_instruction.offset}')
                    # If Rs == Rt, PC += (4 + offset * 4)
                    if rs_data == rt_data:
                        pc_increment = 4 + (offset_data * 4)
                        debugprint(f'\n{rs_data} == {rt_data}. The PC will be incremented by {pc_increment}')
                        program_counter.increment_count(pc_increment)
                    else:
                        debugprint(f'\n{rs_data} != {rt_data}. No branching is done.')
                        program_counter.increment_count(4)
                case 'ADDI':
                    # Fetch the data in Rs
                    rs_data = gpr.load_from_GPR(fetched_instruction.rs)
                    debugprint(f'\n{rs_data} has been fetched from register {fetched_instruction.rs}')
                    const_data = fetched_instruction.constant
                    debugprint(f'\nThe constant is {const_data}')
                    # Perform the addition operation 
                    result = rs_data + const_data
                    debugprint(f'\n{const_data} + {rs_data} = {result}')
                    # Store the result in the specified Rd address
                    gpr.store_into_GPR(fetched_instruction.rd, result)
                    debugprint(f'\n{result} is now stored in register {fetched_instruction.rd}')
                    program_counter.increment_count(4)
                case 'ANDI':
                    # Fetch the data in Rs
                    rs_data = gpr.load_from_GPR(fetched_instruction.rs)
                    debugprint(f'\n{rs_data} has been fetched from register {fetched_instruction.rs}')
                    const_data = fetched_instruction.constant
                    debugprint(f'\nThe constant is {const_data}')
                    # Perform the bitwise AND operation 
                    result = rs_data & const_data
                    debugprint(f'\n{const_data} AND {rs_data} = {result}')
                    # Store the result in the specified Rd address
                    gpr.store_into_GPR(fetched_instruction.rd, result)
                    debugprint(f'\n{result} is now stored in register {fetched_instruction.rd}')
                    program_counter.increment_count(4)
                case 'ORI':
                    # Fetch the data in Rs
                    rs_data = gpr.load_from_GPR(fetched_instruction.rs)
                    debugprint(f'\n{rs_data} has been fetched from register {fetched_instruction.rs}')
                    const_data = fetched_instruction.constant
                    debugprint(f'\nThe constant is {const_data}')
                    # Perform the bitwise OR operation 
                    result = rs_data | const_data
                    debugprint(f'\n{const_data} OR {rs_data} = {result}')
                    # Store the result in the specified Rd address
                    gpr.store_into_GPR(fetched_instruction.rd, result)
                    debugprint(f'\n{result} is now stored in register {fetched_instruction.rd}')
                    program_counter.increment_count(4)
                case 'J':
                    # Fetch target address 
                    target_address = fetched_instruction.address
                    debugprint(f'\nThe target address is {target_address} * 4. The address to jump to in the Memory Address is {target_address * 4}')
                    program_counter.jump_count(target_address * 4)
                case 'JAL':
                    # Fetch target address 
                    target_address = fetched_instruction.address
                    debugprint(f'\nThe target address is {target_address} * 4. The address to jump to in the Memory Address is {target_address * 4}')
                    pc_increment = program_counter.see_count() + 4
                    gpr.store_into_GPR(31, pc_increment)
                    program_counter.jump_count(target_address * 4)
                case 'JR':
                    target_address = gpr.load_from_GPR(31)
                    debugprint(f'\nThe Program Counter will be reset back to the memory address stored in $ra (R31), which is {target_address}')
                    program_counter.jump_count(target_address)
                case 'LW':
                    # Pass into the Memory Address the address stored in register Rs + offset
                    memory_address = gpr.load_from_GPR(fetched_instruction.rs)
                    if fetched_instruction.offset != None:
                        memory_address += fetched_instruction.offset
                    debugprint(f'\nThe Control will fetch the data stored in memory address {memory_address}')
                    if memory_address % 4 != 0:
                        raise KeyError('Invalid memory address {memory_address}. Memory address should be in multiples of 4.')
                    # Load the data from the memory address pointed by the Memory Address into the Data Register, and then into Rd 
                    # Check if cache memory is active
                    data_register = None
                    if memory.cache_active: 
                        debugprint(f'\nAs cache is active, the Control will check if the memory address exists in the cache')
                        # Check if cache.load_from_cache(memory_address) is not None
                        data_register = cache.load_from_cache(memory_address)
                        if data_register:
                            # fetch cache data 
                            debugprint(f'\nThe memory address {memory_address} is found in cache. The Control will fetch the data from cache.')
                        else:
                            # if cache.load_from_cache(memory_address) returns None, fetch data from main memory and write to cache
                            debugprint(f'\nThe memory address {memory_address} is NOT found in cache. The Control will fetch the data from main memory and write the data to cache.')
                            data_register = memory.load_from_memory(memory_address)
                            cache.store_into_cache(memory_address, data_register,memory)
                    else:
                        # if cache memory is not active, fetch data from main memory
                        debugprint(f'\nAs cache is NOT active, the Control will fetch the data from the main memory.')
                        data_register = memory.load_from_memory(memory_address)
                    destination_register = fetched_instruction.rd
                    debugprint(f'\nThe Control will save {data_register} into register {destination_register}')
                    gpr.store_into_GPR(destination_register, data_register)
                    program_counter.increment_count(4)
                case 'SW':
                    # Pass in the Memory address the address stored in register Rt + offset
                    rt = fetched_instruction.rt
                    memory_address = gpr.load_from_GPR(rt)
                    if fetched_instruction.offset != None:
                        memory_address += fetched_instruction.offset
                    debugprint(f'\nThe memory address stored in register {fetched_instruction.rt} (with applicable offset) is {memory_address}')
                    if memory_address % 4 != 0:
                        raise KeyError('Invalid memory address {memory_address}. Memory address should be in multiples of 4.')
                    # Pass into Data Register the data in Rs 
                    data_register = gpr.load_from_GPR(fetched_instruction.rs)
                    debugprint(f'\nThe data {data_register} has been fetched from register {fetched_instruction.rs}')
                    # Check if cache is turned on
                    if memory.cache_active: 
                        debugprint(f'\nAs cache is turned on, the data {data_register} will be stored in cache tagged with the memory address {memory_address}')
                        # Write the data to cache
                        cache.store_into_cache(memory_address, data_register,memory)
                    else:
                        # Save the data in Data Register into the address pointed by the Memory Address
                        debugprint(f'\nAs cache is turned off, the data {data_register} will be stored in the main memory address {memory_address}')
                        memory.store_into_memory(memory_address,data_register)
                    program_counter.increment_count(4)
                case 'CACHE':
                    if fetched_instruction.cache_bool == 1:
                        memory.cache_active = True 
                        debugprint('\nCache memory is activated.')
                    elif fetched_instruction.cache_bool == 0:
                        memory.cache_active = False
                        debugprint('\nCache memory is deactivated.')
                    program_counter.increment_count(4)
                case 'HALT':
                    debugprint(f'\nThe program is terminated due to the HALT instruction')
                    break
        else:
            debugprint(f'\nThe fetched data from memory address {program_counter.see_count()} is not an instruction. The PC will increment.')
            program_counter.increment_count(4)
    if program_counter.see_count() >stop_count:
        debugprint(f'\nThe Program Counter has reached count {program_counter.see_count()}.')
        debugprint(f'\nThe Control has inspected all memory addresses. The program now ends.')

if __name__ == '__main__':
    # Initialise PC 
    pc = Program_Counter()

    # Initialise Memory
    main_memory = Memory()

    # Run argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('instruction_file', help = "Name of .txt file that contains the MIPS instructions to be uploaded into the program")
    parser.add_argument('-d', '--debug_print', type = int, help = "0 turns off default debug print")
    args = parser.parse_args()
    instruction_txt = args.instruction_file
    debug_bool = args.debug_print
    if debug_bool == 0:
        is_debug = False
    main_memory.load_instructions_into_memory(instruction_txt)

    # Initialise Cache
    cache_memory = Cache()

    # Initialise GPR 
    gpr = GPR()

    # Run control()
    control(pc,main_memory,cache_memory,gpr)
    gpr.print_register()
    main_memory.print_memory()
    cache_memory.print_cache()
