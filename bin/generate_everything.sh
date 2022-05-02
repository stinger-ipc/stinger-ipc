#!/bin/sh

BASE_DIR=$(dirname $0)

# Python
python3 ${BASE_DIR}/python_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/python/
python3 ${BASE_DIR}/python_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/python/
python3 ${BASE_DIR}/python_generator.py ${BASE_DIR}/../example_interfaces/enum_only/enum_only.stingeripc ${BASE_DIR}/../example_interfaces/enum_only/output/python/

# Rust
python3 ${BASE_DIR}/rust_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/rust/
python3 ${BASE_DIR}/rust_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/rust/
(cd ${BASE_DIR}/../example_interfaces/full/output/rust/ && cargo build)

# C++
python3 ${BASE_DIR}/cpp_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/cpp/
python3 ${BASE_DIR}/cpp_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/cpp/
if [ ! -d "${BASE_DIR}/../example_interfaces/full/output/cpp/build" ]; then
    mkdir ${BASE_DIR}/../example_interfaces/full/output/cpp/build
fi
(cd ${BASE_DIR}/../example_interfaces/full/output/cpp/build && cmake .. && make)

# AsyncAPI
python3 ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/enum_only/enum_only.stingeripc ${BASE_DIR}/../example_interfaces/enum_only/output/asyncapi/
python3 ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/asyncapi/
python3 ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/asyncapi/