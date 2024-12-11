#!/usr/bin/env bash

# Remember bash history on the local machine.
ln -s "$(pwd)/.devcontainer/.bash_history" ~/.bash_history

# Install the user's dotfiles from GitHub.
gh repo clone dotfiles ~/.dotfiles && ~/.dotfiles/install.sh

# Copy .env.example to .env if necessary.
if [ ! -f ".env" ]; then
    cp .env.example .env
fi
if [ ! -f ".devcontainer/.env" ]; then
    cp .devcontainer/.env.example .devcontainer/.env
fi

# Create a virtual environment for the project if one doesn't exist.
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate the virtual environment.
echo "source \"$(pwd)/.venv/bin/activate\"" >> ~/.bashrc
