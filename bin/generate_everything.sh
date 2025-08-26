#!/bin/bash

BASE_DIR=$(dirname $0)

# Python


function generate_python() {
    echo
    echo "----------- Generating Python for ${IFACE_NAME} ----------------"
    IFACE_NAME=$1
    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/python/
    uv run pythongen ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stinger.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/python/
    #uv run mypy ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/python/
    uv run black ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/python/
}

generate_python signal_only
generate_python full
generate_python weather

# C++


function generate_cpp() {
    echo
    echo "----------- Generating C++ for ${IFACE_NAME}----------------"
    IFACE_NAME=$1
    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/build
    uv run ${BASE_DIR}/cpp_generator.py ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stinger.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/
    if [ $? -eq 0 ]; then
        (cd ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/build && cmake .. -DCMAKE_BUILD_TYPE=Debug && make)
    fi
}

generate_cpp full
generate_cpp signal_only
generate_cpp weather

# Rust

function generate_rust() {
    echo
    echo "----------- Generating Rust for ${IFACE_NAME}----------------"
    IFACE_NAME=$1
    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/
    uv run rustgen ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stinger.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/
    if [ $? -eq 0 ]; then
        (cd ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/ && cargo build --example client)
        (cd ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/ && cargo build --example ${IFACE_NAME}_server_example)
    fi
}

generate_rust signal_only
generate_rust full
generate_rust weather

(cd ${BASE_DIR}/../example_interfaces/full/output/rust/ && cargo build --example pub_and_recv)

# AsyncAPI
#echo "----------- Creating AsyncAPI Spec ----------------"
#mkdir -p ${BASE_DIR}/../example_interfaces/enum_only/output/asyncapi/
#mkdir -p ${BASE_DIR}/../example_interfaces/full/output/asyncapi/
#mkdir -p ${BASE_DIR}/../example_interfaces/signal_only/output/asyncapi/
#uv run ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/enum_only/enum_only.stingeripc ${BASE_DIR}/../example_interfaces/enum_only/output/asyncapi/
#uv run ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/full/full.stingeripc ${BASE_DIR}/../example_interfaces/full/output/asyncapi/
#uv run ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/asyncapi/

# Markdown

function generate_markdown() {
    echo
    echo "----------- Creating Markdown Document for ${IFACE_NAME}----------------"
    IFACE_NAME=$1

    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/markdown/
    uv run markdowngen ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stinger.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/markdown/
}

generate_markdown full
generate_markdown weather