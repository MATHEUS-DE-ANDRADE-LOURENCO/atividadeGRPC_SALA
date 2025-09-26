cmake_minimum_required(VERSION 3.15)
project(grpc_url_cliente)

set(CMAKE_CXX_STANDARD 17)

find_package(Protobuf REQUIRED)
find_package(gRPC REQUIRED)

# Inclui scripts auxiliares do gRPC para geração automática
include(FindProtobuf)
include(FindPackageHandleStandardArgs)
include(${gRPC_SOURCE_DIR}/cmake/protobuf.cmake)
include(${gRPC_SOURCE_DIR}/cmake/grpc.cmake)

set(PROTO_SRC urls.proto)
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${PROTO_SRC})
protobuf_generate_grpc_cpp(GRPC_SRCS GRPC_HDRS ${PROTO_SRC})

add_executable(cliente main.cpp
    ${PROTO_SRCS}
    ${PROTO_HDRS}
    ${GRPC_SRCS}
    ${GRPC_HDRS}
)

target_include_directories(cliente PRIVATE
    ${Protobuf_INCLUDE_DIRS}
    ${gRPC_INCLUDE_DIRS}
    ${CMAKE_CURRENT_BINARY_DIR}
)

target_link_libraries(cliente
    gRPC::grpc++
    protobuf::libprotobuf
)
