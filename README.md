# pianopy
A python library/application to play, compose and interface with virtual and 
real pianos using MIDI.

## Run tests, build, publish
1. Run the unittests:  
`make test`
2. Build the package as a wheel:  
`make build`
3. Publish the package to pypi
`make publish`

## Development setup
1. Make sure prerequisites are installed
2. Clone the git repo:  
`git clone https://github.com/PeterPyPan/pianopy`
3. Use make to setup the dev environment:
```
# This sets up a venv in ./.venv using poetry and installs the pre-commit hooks.  
make setup
```

## Prerequisites
1. Install `poetry`  
Verify the poetry installation using:  
`poetry --version`  
Installation instructions: https://python-poetry.org/docs/#installation.

2. Install `make`
Verify the make installation using:  
`make --version`  

```
# Installation for OSX
# remove previous installation of command line tools
rm -rf /Library/Developer/CommandLineTools/
# install command line tools
xcode-select --install
# setup command line tools
sudo xcode-select --switch /Library/Developer/CommandLineTools/
```
