#!/bin/bash

echo "Setting up Simple System Monitor..."
echo "=================================================="

print_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

print_success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

print_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

print_warning() {
    echo -e "\033[1;33m[WARNING]\033[0m $1"
}

if ! command -v python3 &> /dev/null; then
    print_error "Python3 is not installed!"
    echo "Installing Python3..."
    
    # Detect OS and install Python3
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        sudo apt update && sudo apt install -y python3 python3-pip python3-venv
    elif [ -f /etc/redhat-release ]; then
        # RedHat/CentOS/Fedora
        sudo yum install -y python3 python3-pip
    elif [ "$(uname)" == "Darwin" ]; then
        # macOS
        if ! command -v brew &> /dev/null; then
            print_error "Homebrew not found. Please install Homebrew first:"
            echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi
        brew install python3
    elif [ -f /etc/arch-release ]; then
        # Arch Linux
        sudo pacman -S python python-pip
    else
        print_error "Unsupported operating system. Please install Python3 manually."
        exit 1
    fi
    
    # Verify installation
    if ! command -v python3 &> /dev/null; then
        print_error "Failed to install Python3!"
        exit 1
    fi
fi

print_success "Python3 is installed: $(python3 --version)"

if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        print_error "Failed to create virtual environment!"
        exit 1
    fi
    print_success "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

print_info "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are already installed
print_info "Checking dependencies..."
if python -c "import psutil, plotly, pandas" 2>/dev/null; then
    print_success "All dependencies are already installed"
else
    print_info "Installing dependencies..."
    
    # Check if requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found! Creating default one..."
        
        # Create default requirements.txt
        cat > requirements.txt << 'EOF'
            psutil==5.9.6
            plotly==5.18.0
EOF
        print_success "Created default requirements.txt"
    fi
    
    pip install --upgrade pip
    pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        print_error "Failed to install dependencies!"
        exit 1
    fi
    print_success "Dependencies installed successfully"
fi

print_info "Creating directory structure..."
mkdir -p monitoring autohealing utils visualization logs

print_success "Directory structure created:"

python main.py
