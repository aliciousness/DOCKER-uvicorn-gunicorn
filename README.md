# Docker-uvicorn-gunicorn

[**Docker**](https://www.docker.com/) image with [**Uvicorn**](https://www.uvicorn.org/) managed by me for high-performance [**FastAPI**](https://fastapi.tiangolo.com/) web applications in **[Python](https://www.python.org/)** with performance auto-tuning.

# Supported tags and respective Dockerfile links

- [`v0.0.1-3.11-bookworm-slim-python`, `v0.0.1`, `v3.11-slim`, `latest`]

- [`v0.0.1-3.11-bookworm-python`, `v3.11-debian`]

## Features

- **Python**: The base image is python version
- **Utilities**: The image includes utilities like curl, git, vim, zsh, gettext, nmap, and iputils-ping.
- **Zsh**: Zsh is the default shell, and oh-my-zsh (omz) is installed for additional features.
- **Powerlevel10k**: This theme for oh-my-zsh is installed for a better terminal user experience.
- **Syntax Highlighting**: zsh-syntax-highlighting plugin is installed for better command line experience.
- **multi-pltform**: Image made for both amd64 and arm64
- **gunicorn settings**: Config file to easily set and change [gunicorn settings](https://docs.gunicorn.org/en/latest/settings.html#errorlog)
> **IMPORTANT** Shell configuration can be done on project to project basis. Oh-my-zsh is pre-installed as well some helpful plugins
> > Because of the installation of omz there is a default omz configuration at `.zshrc,` one can change configuration by overwriting with there on `.zshrc` file

## Usage
### 🚨 WARNING: You Probably Don't Need this Docker Image

You are probably using **Kubernetes** or similar tools. In that case, you probably **don't need this image** (or any other **similar base image**). You are probably better off **building a Docker image from scratch** as explained in the docs for [FastAPI in Containers - Docker: Build a Docker Image for FastAPI](https://fastapi.tiangolo.com/deployment/docker/#replication-number-of-processes).

---

You can read more about this in the [FastAPI documentation about: FastAPI in Containers - Docker](https://fastapi.tiangolo.com/deployment/docker/#replication-number-of-processes).
You can use this Docker image as a base for your Python projects. It's especially useful if you prefer using zsh and oh-my-zsh in your development environment.

If you want to like to run any pre configurations before the server starts you can add a `prestart` script into the `/app` directory. For example you can add migrations 

```shell
#! /usr/bin/env bash

# Let the DB start
sleep 10;
# Run migrations
alembic upgrade head
```

You can overwrite the default gunicorn config by placing your own gunicorn_conf.py file in the `/app` directory 
