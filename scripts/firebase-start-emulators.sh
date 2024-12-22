#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

DATA_DIR="$SCRIPT_DIR/../firebase_emulator_data"
mkdir -p "$DATA_DIR"

firebase emulators:start --only auth --project="$FIREBASE_PROJECT_ID" --import="$DATA_DIR" --export-on-exit="$DATA_DIR"
