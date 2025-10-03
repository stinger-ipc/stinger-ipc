#!/bin/bash

BASE_DIR=$(dirname $0)

#### Python

function generate_python() {
    echo
    echo "----------- Generating Python for ${IFACE_NAME} ----------------"
    IFACE_NAME=$1
    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/python/
    uv run stinger generate python ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stinger.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/python/
    RC=$?
    if [ $RC -ne 0 ]; then return $RC; fi
    uv run black ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/python/
    return 0
}

generate_python signal_only || exit 1
generate_python full || exit 1
#generate_python weather || exit 1

#### C++

function generate_cpp() {
    echo
    echo "----------- Generating C++ for ${IFACE_NAME}----------------"
    IFACE_NAME=$1
    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/build
    uv run stinger generate cpp ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stinger.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/
    RC=$?
    if [ $RC -ne 0 ]; then return $RC; fi
    which clang-format &> /dev/null
    if [ $? -eq 0 ]; then
        echo "Running clang-format on generated C++ files"
        clang-format --style=file:${BASE_DIR}/../clang-format-config.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/include/*.hpp ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/src/*.cpp ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/examples/*.cpp -i
    fi
    if [ $? -eq 0 ]; then
        (cd ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/build && cmake .. -DCMAKE_BUILD_TYPE=Debug && make -j4)
    fi
    return 0
}

generate_cpp full || exit 1
generate_cpp signal_only || exit 1
#generate_cpp weather || exit 1

#### Rust

function generate_rust() {
    echo
    echo "----------- Generating Rust for ${IFACE_NAME}----------------"
    IFACE_NAME=$1
    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/
    uv run stinger generate rust ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stinger.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/
    RC=$?
    if [ $RC -eq 0 ]; then
        (cd ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/ && cargo update)
        (cd ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/ && cargo fmt)
        (cd ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/ && cargo check)
        (cd ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/ && cargo check --example ${IFACE_NAME}_client_demo --features client)
        (cd ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/ && cargo check --example ${IFACE_NAME}_server_demo --features server)
    fi
    return $RC
}

generate_rust signal_only || exit 1
generate_rust full || exit 1
#generate_rust weather || exit 1

(cd ${BASE_DIR}/../example_interfaces/full/output/rust/ && cargo build --example full_connection_demo --features payloads)

# AsyncAPI
#echo "----------- Creating AsyncAPI Spec ----------------"
#mkdir -p ${BASE_DIR}/../example_interfaces/enum_only/output/asyncapi/
#mkdir -p ${BASE_DIR}/../example_interfaces/full/output/asyncapi/
#mkdir -p ${BASE_DIR}/../example_interfaces/signal_only/output/asyncapi/
#uv run ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/enum_only/enum_only.stingeripc ${BASE_DIR}/../example_interfaces/enum_only/output/asyncapi/
#uv run ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/full/full.stingeripc ${BASE_DIR}/../example_interfaces/full/output/asyncapi/
#uv run ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/asyncapi/

#### Markdown

function generate_markdown() {
    echo
    echo "----------- Creating Markdown Document for ${IFACE_NAME}----------------"
    IFACE_NAME=$1

    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/markdown/
    uv run stinger generate markdown ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stinger.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/markdown/
}

generate_markdown full
generate_markdown weather
generate_markdown signal_only

#### HTML/JS/CSS

function generate_web() {
    echo
    echo "----------- Creating Webpage Interface for ${IFACE_NAME}----------------"
    IFACE_NAME=$1

    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/web/
    uv run stinger generate web ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stinger.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/web/
}

generate_web full
generate_web weather
generate_web signal_only
