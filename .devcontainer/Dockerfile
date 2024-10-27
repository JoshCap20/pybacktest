# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set environment variables for timezone and frontend
ENV TZ=America/New_York
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install system dependencies
RUN apt-get update && apt-get install --yes \
    apt-transport-https \
    ca-certificates \
    curl \
    debian-keyring \
    debian-archive-keyring \
    git \
    gnupg \
    postgresql-client \
    software-properties-common \
    sudo \
    tzdata \
    wget \
    zsh \
    libsqlite3-dev && \
    rm -rf /var/lib/apt/lists/*

# Add Python repository and install Python 3.11 along with essential libraries
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    apt install --yes \
    python3.11 \
    python3-pip \
    python3.11-dev \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/* && \
    unlink /usr/bin/python3 && \
    ln -s /usr/bin/python3.11 /usr/bin/python3

# Set up user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /usr/bin/zsh && \
    echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Git configuration
RUN git config --system core.editor "code --wait" && \
    git config --system safe.directory '/workspace'

# Set user and home environment variables
USER $USERNAME
ENV HOME /home/$USERNAME

# Install oh-my-zsh for the user
RUN curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh | bash - && \
    sed -i 's/robbyrussell/kennethreitz/g' ~/.zshrc && \
    echo 'export PATH=$PATH:$HOME/.local/bin' >>~/.zshrc

# Install Python dependencies listed in requirements.txt (placed at project root)
COPY requirements.txt /workspace/requirements.txt
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r /workspace/requirements.txt

# Set the workspace folder for vscode
WORKDIR /workspace
