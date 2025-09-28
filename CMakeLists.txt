cmake_minimum_required(VERSION 3.10)
project(encurtador_grpc CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(Protobuf REQUIRED)
find_package(gRPC REQUIRED)

# Encontra executáveis
find_program(PROTOC_EXECUTABLE protoc)
if(NOT PROTOC_EXECUTABLE)
  message(FATAL_ERROR "protoc não encontrado. Instale protobuf-compiler.")
endif()

find_program(GRPC_CPP_PLUGIN grpc_cpp_plugin)
if(NOT GRPC_CPP_PLUGIN)
  message(FATAL_ERROR "grpc_cpp_plugin não encontrado. Instale pacote libgrpc-dev / protobuf-compiler-grpc")
endif()

set(PROTO_FILE ${CMAKE_CURRENT_SOURCE_DIR}/urls.proto)
set(GENERATED_SRC ${CMAKE_CURRENT_BINARY_DIR}/urls.pb.cc ${CMAKE_CURRENT_BINARY_DIR}/urls.grpc.pb.cc)
set(GENERATED_HDR ${CMAKE_CURRENT_BINARY_DIR}/urls.pb.h ${CMAKE_CURRENT_BINARY_DIR}/urls.grpc.pb.h)

add_custom_command(
  OUTPUT ${GENERATED_SRC} ${GENERATED_HDR}
  COMMAND ${PROTOC_EXECUTABLE} --cpp_out=${CMAKE_CURRENT_BINARY_DIR} -I ${CMAKE_CURRENT_SOURCE_DIR} ${PROTO_FILE}
  COMMAND ${PROTOC_EXECUTABLE} --grpc_out=${CMAKE_CURRENT_BINARY_DIR} --plugin=protoc-gen-grpc=${GRPC_CPP_PLUGIN} -I ${CMAKE_CURRENT_SOURCE_DIR} ${PROTO_FILE}
  DEPENDS ${PROTO_FILE}
  COMMENT "Gerando arquivos .pb.cc e .grpc.pb.cc"
)

add_custom_target(generate_proto ALL DEPENDS ${GENERATED_SRC} ${GENERATED_HDR})

include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(${Protobuf_INCLUDE_DIRS})

add_executable(cliente_cpp cliente.cpp ${GENERATED_SRC})
target_link_libraries(cliente_cpp PRIVATE protobuf::libprotobuf gRPC::grpc++)
add_dependencies(cliente_cpp generate_proto)