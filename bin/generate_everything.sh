#!/bin/sh

BASE_DIR=$(dirname $0)

python3 ${BASE_DIR}/python_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/python/
python3 ${BASE_DIR}/python_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/python/
python3 ${BASE_DIR}/python_generator.py ${BASE_DIR}/../example_interfaces/enum_only/enum_only.stingeripc ${BASE_DIR}/../example_interfaces/enum_only/output/python/

python3 ${BASE_DIR}/rust_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/rust/
python3 ${BASE_DIR}/rust_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/rust/

python3 ${BASE_DIR}/cpp_generator.py ${BASE_DIR}/../example_interfaces/signal_only/signal_only.stingeripc ${BASE_DIR}/../example_interfaces/signal_only/output/cpp/
python3 ${BASE_DIR}/cpp_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/cpp/

python3 ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/enum_only/enum_only.stingeripc ${BASE_DIR}/../example_interfaces/enum_only/output/asyncapi/
python3 ${BASE_DIR}/asyncapi_generator.py ${BASE_DIR}/../example_interfaces/full/example.stingeripc ${BASE_DIR}/../example_interfaces/full/output/asyncapi/