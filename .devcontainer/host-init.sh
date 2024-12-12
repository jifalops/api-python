#!/usr/bin/env bash

# Copy .env.example to .env if necessary.
if [ ! -f ".env" ]; then
    cp .env.example .env
fi
if [ ! -f ".devcontainer/.env" ]; then
    cp .devcontainer/.env.example .devcontainer/.env
fi
