project(LSMAmerPut)
cmake_minimum_required(VERSION 3.5)

set(PSEUDO_RANDOM On CACHE Bool "Whether to use pseudo random number generator")
if(PSEUDO_RANDOM)
    add_definitions(-DPSEUDO_RANDOM)
endif(PSEUDO_RANDOM)

add_executable(LSMAmerPut main.c arguments.c utilities.c)
target_link_libraries(LSMAmerPut m gsl gslcblas)
