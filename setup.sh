#!/bin/bash

# Error handling function
error_exit() {
    echo "Error: $1"
    read -p "Press [Enter] to exit..."
    exit 1
}

echo "Setup starting..."

# Check for Python interpreter
if python3 --version > /dev/null 2>&1; then
    PYTHON_CMD="python3"
elif python --version > /dev/null 2>&1; then
    PYTHON_CMD="python"
else
    error_exit "Python could not be found."
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv || error_exit "Failed to create virtual environment."
else
    echo "Virtual environment already exists."
fi

# Install dependencies
echo "Installing Python dependencies..."
./venv/bin/python -m pip install -r requirements.txt --quiet --disable-pip-version-check
if [ $? -ne 0 ]; then
    error_exit "Python dependencies installation failed."
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "Creating .env configuration..."
        cp .env.example .env > /dev/null 2>&1
    fi
fi

# Install Node.js dependencies
if command -v npm &> /dev/null; then
    echo "Installing Node.js dependencies..."
    if npm ci --silent --no-audit --no-fund > /dev/null 2>&1; then
        : # Success, do nothing
    else
        error_exit "Node.js dependencies installation failed."
    fi
else
    echo "Warning: npm not found. Node.js dependencies were not installed."
fi

echo -e "\nSetup complete.\n"
exit 0
