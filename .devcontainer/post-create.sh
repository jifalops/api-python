#!/usr/bin/env bash

# Remember bash history on the local machine.
ln -s "$(pwd)/.devcontainer/.bash_history" ~/.bash_history

# Install the user's dotfiles from GitHub.
gh repo clone dotfiles ~/.dotfiles && ~/.dotfiles/install.sh

# Create a virtual environment for the project if one doesn't exist.
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate the virtual environment.
echo "source \"$(pwd)/.venv/bin/activate\"" >> ~/.bashrc

# Add bash completion for the Stripe CLI.
mkdir -p ~/.local/share/bash-completion/completions && \
stripe completion --shell bash > /dev/null && \
mv stripe-completion.bash ~/.local/share/bash-completion/completions/stripe