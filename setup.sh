#!/usr/bin/bash
echo "Upgrading pip"
pip3 install --upgrade pip

echo "Initializing submodules"
git submodule init

echo "Creating submodule folders"
git submodule update

echo "Installing dependencies"
pip3 install -r requirements.txt

echo "Installing requirements for dscore"
cd ThirdPartyTools/dscore
pip3 install -r requirements.txt
echo "Installation complete"

echo "Installing pyannote-audio"
cd ../pyannote-audio
pip3 install -r requirements.txt
pip3 install .
echo "Installation complete"

echo "Install PyTorch"
pip3 install torch torchvision
echo "Installation complete"
