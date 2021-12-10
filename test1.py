from script import Memory, Instruction, Cache, GPR, Program_Counter, control

# Initialise PC 

pc = Program_Counter()

# Initialise Memory

main_memory = Memory()

# Initialise Cache

cache_memory = Cache()

# Initialise GPR 

gpr = GPR()

# Tests

# make a test instruction 

test_add_instruction = Instruction('ADD,1,4,5')
test_sub_instruction = Instruction('SUB,2,1,5')
test_mult_instruction = Instruction('MULT,3,5,1')
test_and_instruction = Instruction('AND,8,5,3')
test_or_instruction = Instruction('OR,2,1,3')
test_slt1_instruction = Instruction('SLT,10,4,5')
test_slt2_instruction = Instruction('SLT,11,3,5')
test_beq_instruction = Instruction('BEQ,2,4,5')
test_addi_instruction = Instruction('ADDI,13,0,987')
test_andi_instruction = Instruction('ANDI,14,3,1000')
test_ori_instruction = Instruction('ORI,12,13,100')
test_jump_instruction = Instruction('J,15')
test_jal_instruction = Instruction('JAL,25')
test_jr_instruction = Instruction('JR,31')
test_lw_instruction = Instruction('LW,20,114(3)')
test_lw2_instruction = Instruction('LW,22,21')
test_sw_instruction = Instruction('SW,22,122(5)')
test_halt_instruction = Instruction('HALT')
# add test instruction into memory 

main_memory.store_into_memory(0,test_add_instruction)
main_memory.store_into_memory(4,test_sub_instruction)
main_memory.store_into_memory(8,'Random data 1234')
main_memory.store_into_memory(16,test_mult_instruction)
main_memory.store_into_memory(20,test_and_instruction)
main_memory.store_into_memory(24,test_or_instruction)
main_memory.store_into_memory(28,test_slt1_instruction)
main_memory.store_into_memory(32,test_slt2_instruction)
main_memory.store_into_memory(36,test_beq_instruction)
main_memory.store_into_memory(40,test_addi_instruction)
main_memory.store_into_memory(44,test_andi_instruction)
main_memory.store_into_memory(48,test_ori_instruction)
main_memory.store_into_memory(52,test_jal_instruction)
main_memory.store_into_memory(100,test_lw_instruction)
main_memory.store_into_memory(104,test_jr_instruction)
main_memory.store_into_memory(56,test_lw2_instruction)
main_memory.store_into_memory(60,test_lw2_instruction)
main_memory.store_into_memory(64,test_sw_instruction)
main_memory.store_into_memory(72,test_halt_instruction)
main_memory.store_into_memory(200,5000)
main_memory.store_into_memory(240,'Random data 987')
main_memory.store_into_memory(120,10000)

# add test data into GPR

gpr.store_into_GPR(4,1)
gpr.store_into_GPR(5,2)
gpr.store_into_GPR(21,240)

# Addition test 


control(pc, main_memory, cache_memory, gpr)
gpr.print_register()
main_memory.print_memory()
