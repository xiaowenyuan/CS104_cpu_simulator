from script import Memory, Instruction, Cache, GPR, Program_Counter, control

# Initialise PC 

pc = Program_Counter()

# Initialise Memory

main_memory = Memory()

# Initialise Cache

cache_memory = Cache()

# Initialise GPR 

gpr = GPR()

gpr.store_into_GPR(7,236)
gpr.store_into_GPR(9,200)
main_memory.store_into_memory(236, 1000)
main_memory.store_into_memory(0, Instruction('CACHE,1'))
main_memory.store_into_memory(4, Instruction('LW,1,7'))
main_memory.store_into_memory(8, Instruction('LW,2,36(9)'))
main_memory.store_into_memory(12, Instruction('ADDI,1,0,4'))
main_memory.store_into_memory(16, Instruction('ADDI,3,0,10'))
main_memory.store_into_memory(20, Instruction('SUB,11,7,1'))
main_memory.store_into_memory(24, Instruction('SW,3,7'))
main_memory.store_into_memory(28, Instruction('SW,11,4(9)'))
main_memory.store_into_memory(32, Instruction('SW,0,9'))
main_memory.store_into_memory(36, Instruction('SW,3,1'))
main_memory.store_into_memory(40, Instruction('SW,0,8(7)'))
main_memory.store_into_memory(44, Instruction('HALT,;'))

control(pc,main_memory,cache_memory,gpr)

gpr.print_register()
main_memory.print_memory()
cache_memory.print_cache()