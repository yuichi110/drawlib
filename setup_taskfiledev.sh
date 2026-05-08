#!/bin/bash

if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! command -v brew &>/dev/null; then
        echo "Homebrew is not installed. Please install it first: https://brew.sh/"
        exit 1
    fi

    echo "Checking for go-task..."
    if brew list go-task &>/dev/null; then
        echo "go-task is already installed. Upgrading..."
        brew upgrade go-task
    else
        echo "Installing go-task..."
        brew install go-task
    fi
else
    echo "Please install go-task manually for your platform."
    echo "Visit https://taskfile.dev/installation/ for instructions."
fi
