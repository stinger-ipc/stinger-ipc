#!/bin/sh

BASE_DIR=$(dirname $0)

# Python
echo "----------- Generating Python ----------------"
mkdir -p ${BASE_DIR}/../example_interfaces/signal_only/output/python/
mkdir -p ${BASE_DIR}/../example_interfaces/full/output/python/
mkdir -p ${BASE_DIR}/../example_interfaces/enum_only/output/python/
python3 ${BASE_DIR}/python_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/python/
python3 ${BASE_DIR}/python_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/python/
python3 ${BASE_DIR}/python_generator.py ${BASE_DIR}/../example_interfaces/enum_only/enum_only.stingeripc ${BASE_DIR}/../example_interfaces/enum_only/output/python/

# Rust
echo "----------- Generating Rust ----------------"
#rm -rf ${BASE_DIR}/../example_interfaces/full/output/rust/ ${BASE_DIR}/../example_interfaces/signal_only/output/rust/
python3 ${BASE_DIR}/rust_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/rust/
python3 ${BASE_DIR}/rust_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/rust/
if [ $? -eq 0 ]; then
    (cd ${BASE_DIR}/../example_interfaces/full/output/rust/ && cargo build --example client)
    (cd ${BASE_DIR}/../example_interfaces/full/output/rust/ && cargo build --example server)
    (cd ${BASE_DIR}/../example_interfaces/signal_only/output/rust/ && cargo build --example client)
    (cd ${BASE_DIR}/../example_interfaces/signal_only/output/rust/ && cargo build --example server)
fi

# C++
echo "----------- Generating C++ ----------------"
python3 ${BASE_DIR}/cpp_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/cpp/
python3 ${BASE_DIR}/cpp_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/cpp/
if [ $? -eq 0 ]; then
    if [ ! -d "${BASE_DIR}/../example_interfaces/full/output/cpp/build" ]; then
        mkdir ${BASE_DIR}/../example_interfaces/full/output/cpp/build
    fi
    (cd ${BASE_DIR}/../example_interfaces/full/output/cpp/build && cmake .. -DCMAKE_BUILD_TYPE=Debug && make)

    if [ ! -d "${BASE_DIR}/../example_interfaces/signal_only/output/cpp/build" ]; then
        mkdir ${BASE_DIR}/../example_interfaces/signal_only/output/cpp/build
    fi
    (cd ${BASE_DIR}/../example_interfaces/signal_only/output/cpp/build && cmake .. -DCMAKE_BUILD_TYPE=Debug && make)
fi

# AsyncAPI
echo "----------- Creating AsyncAPI Spec ----------------"
mkdir -p ${BASE_DIR}/../example_interfaces/enum_only/output/asyncapi/
mkdir -p ${BASE_DIR}/../example_interfaces/full/output/asyncapi/
mkdir -p ${BASE_DIR}/../example_interfaces/signal_only/output/asyncapi/
python3 ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/enum_only/enum_only.stingeripc ${BASE_DIR}/../example_interfaces/enum_only/output/asyncapi/
python3 ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/asyncapi/
python3 ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/asyncapi/