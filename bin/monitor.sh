#!/bin/bash

mosquitto_sub -v -V 5 \
    -t '+/+/method/+' \
    -t 'client/#' \
    -t '+/+/property/#' \
    -t '+/+/interface' \
    -F '%U %t\n%p\nContentType: %C\nResponseTopic: %R\nUserProperties: %P\n-----------------'
