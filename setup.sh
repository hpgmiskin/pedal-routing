CWD=$(pwd)

# Install Libosmium
cd lib/libosmium
mkdir -p build
cd build
cmake ..
make
cd $CWD

# Install Pysmium
cd lib/pyosmium 
python setup.py build
python setup.py install
cd $CWD