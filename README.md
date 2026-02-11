# gridcode

A simple grid-based simulation framework for computational exploration.

## Installation

### Prerequisites

**Racket 8.0+**

All platforms:

Download from [racket-lang.org](https://racket-lang.org/) or

macOS:
```bash
brew install racket
```

Linux (Ubuntu/Debian):
```bash
sudo apt install racket
```

Linux (Fedora/RHEL):
```bash
sudo dnf install racket
```

### Get the Project
```bash
git clone https://github.com/antfarm/gridcode.git
cd gridcode
```

### Install the Package
```bash
raco pkg install --link ../gridcode
```

## Usage

Programs are written using the GridCode DSL in `.grid` files with the `#lang gridcode` language. For reference, have a look at the [example programs](/examples).

Run the examples:
```bash
# Conway's Game of Life
./bin/gridcode examples/life.grid

# Pong
./bin/gridcode examples/pong.grid

# Ant
./bin/gridcode examples/ant.grid

# Hello
./bin/gridcode examples/hello.grid
```