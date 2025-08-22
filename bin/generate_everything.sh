#!/bin/bash

BASE_DIR=$(dirname $0)

# Python
echo "----------- Generating Python ----------------"

function generate_python() {
    IFACE_NAME=$1
    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/python/
    uv run ${BASE_DIR}/python_generator.py ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stingeripc ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/python/
}

generate_python signal_only
generate_python full
generate_python weather

# C++
echo
echo "----------- Generating C++ ----------------"

function generate_cpp() {
    IFACE_NAME=$1
    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/build
    uv run ${BASE_DIR}/cpp_generator.py ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stingeripc ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/
    if [ $? -eq 0 ]; then
        (cd ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/build && cmake .. -DCMAKE_BUILD_TYPE=Debug && make)
    fi
}

generate_cpp full
generate_cpp signal_only

# Rust
echo
echo "----------- Generating Rust ----------------"

function generate_rust() {
    IFACE_NAME=$1
    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/
    uv run ${BASE_DIR}/rust_generator.py ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stingeripc ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/
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
echo
echo "----------- Creating Markdown Documents ----------------"

function generate_markdown() {
    IFACE_NAME=$1

    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/markdown/
    uv run ${BASE_DIR}/markdown_generator.py ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stingeripc ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/markdown/
}

generate_markdown full
generate_markdown weather