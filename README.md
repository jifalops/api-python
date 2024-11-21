# FastAPI-Docker Template

A template repo for a rich dev-container for developing a FastAPI backend that deploys to a Docker container.

## Features

1. A python base devcontainer for a consistent development environment.
    1. Based on Microsoft's [devcontainer][1] spec.
    1. Uses the host's timezone (`$TZ`) and Github CLI token (`$GITHUB_TOKEN`).
    1. If `$GITHUB_TOKEN` is set, it will clone the user's `dotfiles` repository and run its `install.sh` after creating the container. See [jifalops/dotfiles][2] for an example.
    1. Local shell history is persisted when rebuilding the container.
1. Integrated terminals when opened with VS Code:
    1. Run unit tests and start the local server.
1. Hexagonal architecture (ports and adapters) with feature-based modules.
    1. Static typing and dependency injection.
1. All config comes from environment variables.
1. Runs locally using docker-compose.yml.
1. Works with Postgres, Neo4j (todo), and MongoDB (todo) databases.
1. Supports JWT, fastapi-users, and Firebase auth out of the box (todo).
1. Github Actions for CI/CD (todo).



[1]: https://github.com/devcontainers/images/tree/main/src/typescript-node
[2]: https://github.com/jifalops/dotfiles
[3]: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
[4]: https://github.com/jifalops/dotfiles/blob/bf9627445abf5ffe25515e8a6d2fe1d1c681e606/.sh_common#L87