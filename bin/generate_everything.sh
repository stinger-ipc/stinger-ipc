#!/bin/sh

BASE_DIR=$(dirname $0)

# Python
echo "----------- Generating Python ----------------"
mkdir -p ${BASE_DIR}/../example_interfaces/signal_only/output/python/
mkdir -p ${BASE_DIR}/../example_interfaces/full/output/python/
mkdir -p ${BASE_DIR}/../example_interfaces/enum_only/output/python/
uv run ${BASE_DIR}/python_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/python/
uv run ${BASE_DIR}/python_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/python/
uv run ${BASE_DIR}/python_generator.py ${BASE_DIR}/../example_interfaces/enum_only/enum_only.stingeripc ${BASE_DIR}/../example_interfaces/enum_only/output/python/

# C++
echo "----------- Generating C++ ----------------"
uv run ${BASE_DIR}/cpp_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/cpp/
uv run ${BASE_DIR}/cpp_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/cpp/
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

# Rust
echo "----------- Generating Rust ----------------"
#rm -rf ${BASE_DIR}/../example_interfaces/full/output/rust/ ${BASE_DIR}/../example_interfaces/signal_only/output/rust/
uv run ${BASE_DIR}/rust_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/rust/
uv run ${BASE_DIR}/rust_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/rust/
if [ $? -eq 0 ]; then
    (cd ${BASE_DIR}/../example_interfaces/full/output/rust/ && cargo build --example client)
    (cd ${BASE_DIR}/../example_interfaces/full/output/rust/ && cargo build --example example_server_example)
    (cd ${BASE_DIR}/../example_interfaces/full/output/rust/ && cargo build --example pub_and_recv)
    (cd ${BASE_DIR}/../example_interfaces/signal_only/output/rust/ && cargo build --example client)
    (cd ${BASE_DIR}/../example_interfaces/signal_only/output/rust/ && cargo build --example signal_only_server_example)
fi

# AsyncAPI
echo "----------- Creating AsyncAPI Spec ----------------"
mkdir -p ${BASE_DIR}/../example_interfaces/enum_only/output/asyncapi/
mkdir -p ${BASE_DIR}/../example_interfaces/full/output/asyncapi/
mkdir -p ${BASE_DIR}/../example_interfaces/signal_only/output/asyncapi/
uv run ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/enum_only/enum_only.stingeripc ${BASE_DIR}/../example_interfaces/enum_only/output/asyncapi/
uv run ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/asyncapi/
uv run ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/asyncapi/

# Markdown
echo "----------- Creating Markdown Documents ----------------"
mkdir -p ${BASE_DIR}/../example_interfaces/full/output/markdown/
uv run ${BASE_DIR}/markdown_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/markdown/
