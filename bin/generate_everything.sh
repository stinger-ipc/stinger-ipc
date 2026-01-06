#!/bin/bash

BASE_DIR=$(dirname $0)
if [ -z "$THREADS" ]; then
    THREADS=16
fi

#### Generate Function

function generate_python() {
    echo
    echo "----------- Generating Python for ${IFACE_NAME} ----------------"
    IFACE_NAME=$1
    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/python/
    uv run stinger generate -l python ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stinger.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/python/
    RC=$?
    if [ $RC -ne 0 ]; then return $RC; fi
    uv run black ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/python/
    return 0
}


function generate_cpp() {
    echo
    echo "----------- Generating C++ for ${IFACE_NAME}----------------"
    IFACE_NAME=$1
    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/build
    uv run stinger generate -l cpp ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stinger.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/
    RC=$?
    if [ $RC -ne 0 ]; then return $RC; fi
    which clang-format &> /dev/null
    if [ $? -eq 0 ]; then
        echo "Running clang-format on generated C++ files"
        clang-format --style=file:${BASE_DIR}/../clang-format-config.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/include/*.hpp ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/src/*.cpp ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/examples/*.cpp -i
    fi
    if [ $? -eq 0 ]; then
        (cd ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/cpp/build && cmake .. -DCMAKE_BUILD_TYPE=Debug && make -j${THREADS})
    fi
    return 0
}

function generate_rust() {
    echo
    echo "----------- Generating Rust for ${IFACE_NAME}----------------"
    IFACE_NAME=$1
    EXAMPLE_PREFIX=$1
    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/
    uv run stinger generate -l rust ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stinger.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/
    RC=$?
    if [ $RC -eq 0 ]; then
        echo "${IFACE_NAME} | cargo update"
        (cd ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/ && cargo update)
        echo "${IFACE_NAME} | cargo fmt"
        (cd ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/ && cargo fmt)
        echo "${IFACE_NAME} | cargo check"
        (cd ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/ && cargo check --features client,server,payloads)
        if [ $? -ne 0 ]; then
            RC=1
        fi
        echo "${IFACE_NAME} | cargo check client_demo"
        (cd ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/ && cargo check --example ${EXAMPLE_PREFIX}_client_demo --features client)
        if [ $? -ne 0 ]; then
            RC=1
        fi
        echo "${IFACE_NAME} | cargo check server_demo"
        (cd ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/rust/ && cargo check --example ${EXAMPLE_PREFIX}_server_demo --features server)
        if [ $? -ne 0 ]; then
            RC=1
        fi
    fi
    return $RC
}

#### Start With Simple

generate_rust simple || exit 1
generate_python simple || exit 1
generate_cpp simple || exit 1

mkdir -p ${BASE_DIR}/../example_interfaces/simple/output-integers/protobuf/
uv run stinger generate -l protobuf --consumer integers ${BASE_DIR}/../example_interfaces/simple/simple.stinger.yaml ${BASE_DIR}/../example_interfaces/simple/output-integers/protobuf/
if [ $? -ne 0 ]; then exit 1; fi

mkdir -p ${BASE_DIR}/../example_interfaces/simple/output-alternate/python/
uv run stinger generate -l python --config ${BASE_DIR}/../example_interfaces/alternates.toml ${BASE_DIR}/../example_interfaces/simple/simple.stinger.yaml ${BASE_DIR}/../example_interfaces/simple/output-alternate/python/
if [ $? -ne 0 ]; then exit 1; fi

#### Python

generate_python signal_only || exit 1
generate_python full || exit 1
generate_python weather || exit 1
generate_python testable || exit 1

#### C++


generate_cpp testable || exit 1
generate_cpp full || exit 1
generate_cpp signal_only || exit 1
generate_cpp weather || exit 1


#### Rust

generate_rust testable || exit 1
generate_rust signal_only || exit 1
generate_rust full || exit 1
generate_rust weather || exit 1

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
    uv run stinger generate -l markdown ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stinger.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/markdown/
}

generate_markdown full
generate_markdown weather
generate_markdown signal_only
generate_markdown testable

#### HTML/JS/CSS

function generate_web() {
    echo
    echo "----------- Creating Webpage Interface for ${IFACE_NAME}----------------"
    IFACE_NAME=$1

    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/web/
    uv run stinger generate -l web ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stinger.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/web/
}

generate_web full
generate_web weather
generate_web signal_only
generate_web testable

#### Protobuf
function generate_protobuf() {
    echo
    echo "----------- Creating Protobuf messages for ${IFACE_NAME}----------------"
    IFACE_NAME=$1

    mkdir -p ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/protobuf/
    uv run stinger generate -l protobuf ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/${IFACE_NAME}.stinger.yaml ${BASE_DIR}/../example_interfaces/${IFACE_NAME}/output/protobuf/
}

generate_protobuf full
generate_protobuf weather
generate_protobuf signal_only
generate_protobuf testable
