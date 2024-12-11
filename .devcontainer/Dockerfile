# https://github.com/jifalops/devcontainers/tree/main/images/python/.devcontainer
FROM jifalops/python:latest

# Install additional packages
RUN export DEBIAN_FRONTEND=noninteractive && sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    trash-cli

# Install neo4j-migrations
RUN VERSION=$(basename $(curl -Ls -o /dev/null -w %{url_effective} https://github.com/michael-simons/neo4j-migrations/releases/latest)) && \
    ZIP_LINUX=https://github.com/michael-simons/neo4j-migrations/releases/download/${VERSION}/neo4j-migrations-${VERSION}-linux-x86_64.zip && \
    curl -L $ZIP_LINUX -o nmig.zip && \
    mkdir -p ~/.local/bin ~/.local/share/bash-completion/completions && \
    unzip -jo nmig.zip "*/bin/neo4j-migrations" -d ~/.local/bin/ && \
    unzip -jo nmig.zip "*/completion/neo4j-migrations_completion" -d ~/.local/share/bash-completion/completions/ && \
    mv ~/.local/share/bash-completion/completions/neo4j-migrations_completion ~/.local/share/bash-completion/completions/neo4j-migrations && \
    rm nmig.zip
