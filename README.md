# Mini Display

A Python package for displaying information on a 64x32 RGB LED matrix with tiny pixel font and colored widgets.

## Features

- **Clock Widget**: Displays time in compact "h:MMa" format with date "MM/DD/YY"
- **Subway Widget**: Shows next MTA subway departures with line colors
- **Weather Widget**: Displays temperature in Celsius from NWS forecast

## Installation

### From PyPI (when published)

```bash
pip install mini-display
```

### For Raspberry Pi with LED Matrix

First, install the HZeller RGB LED Matrix library:

```bash
# Install build dependencies
sudo apt-get update
sudo apt-get install -y python3-dev python3-pillow

# Clone and build the RGB Matrix library
cd ~
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix
make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)
```

Then install the mini-display package:

```bash
pip install mini-display
```

Or install with the optional rpi extras (note: this may not work if rpi-rgb-led-matrix is not on PyPI):

```bash
pip install mini-display[rpi]
```

### From Source

```bash
git clone https://github.com/yourusername/mini-display.git
cd mini-display
pip install -e .
```

## Usage

The RGB LED Matrix requires root access to control the GPIO pins. You have two main options:

### Option 1: Install system-wide (Recommended)

Install the package system-wide so sudo can access it:

```bash
sudo pip install /home/james/md
```

Then run normally with sudo:

```bash
sudo mini-display --rows 32 --cols 64 \
  --station "Jay St-MetroTech" \
  --routes "A,C,F,R" \
  --zip 11201 \
  --cycle-seconds 6 \
  --brightness 70
```

### Option 2: Use sudo with Python path

Keep your user installation and set the Python path for sudo:

```bash
sudo PYTHONPATH=/home/james/.local/lib/python3.9/site-packages python3 -m mini_display.display --rows 32 --cols 64 \
  --station "Jay St-MetroTech" \
  --routes "A,C,F,R" \
  --zip 11201 \
  --cycle-seconds 6 \
  --brightness 70
```

Or add to sudoers to preserve environment:

```bash
# Run once to allow preserving PYTHONPATH:
echo "$USER ALL=(ALL) NOPASSWD: SETENV: /usr/bin/python3" | sudo tee /etc/sudoers.d/mini-display
```

### Command-line Options

### Available Options

- `--rows`: LED matrix rows (default: 32)
- `--cols`: LED matrix columns (default: 64)
- `--chain-length`: Number of chained matrices (default: 1)
- `--parallel`: Parallel chains (default: 1)
- `--hardware-mapping`: Hardware mapping (default: "adafruit-hat")
- `--gpio-slowdown`: GPIO slowdown (default: 2)
- `--pwm-bits`: PWM bits (default: 11)
- `--brightness`: Display brightness 1-100 (default: 70)
- `--cycle-seconds`: Seconds per widget (default: 6)
- `--station`: Subway station name (can be repeated)
- `--routes`: Comma-separated route letters (default: "A,C,F,R")
- `--zip`: ZIP code for weather (default: "11201")
- `--lat`: Latitude for weather (optional)
- `--lon`: Longitude for weather (optional)

## Requirements

- Python 3.8+
- Pillow
- requests
- nyct-gtfs
- protobuf
- rpi-rgb-led-matrix (for Raspberry Pi with LED matrix)

## Hardware

This package is designed for:
- Raspberry Pi (any model with GPIO)
- 64x32 RGB LED Matrix (e.g., Adafruit Product ID: 5036 - 2.5mm pitch)
  - Dimensions: 160mm x 80mm x 14.7mm
  - 2048 bright RGB LEDs (64x32 grid)
  - 1:16 scan rate
- Adafruit RGB Matrix HAT or compatible driver
- Also compatible with other matrix sizes (16x32, 32x32, etc.) by adjusting `--rows` and `--cols`

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.