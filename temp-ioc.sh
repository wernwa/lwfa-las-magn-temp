#!/bin/bash

export EPICS_CA_SERVER_PORT=5064
export EPICS_CA_REPEATER_PORT=5065

./temp-ioc.py
