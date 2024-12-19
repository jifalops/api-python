#!/usr/bin/env bash

# Copy .env.example to .env if necessary.
if [ ! -f ".devcontainer/.env" ]; then
    cp .devcontainer/.env.example .devcontainer/.env
fi
if [ ! -f "scripts/admin/.env" ]; then
    cp scripts/admin/.env.example scripts/admin/.env
fi

