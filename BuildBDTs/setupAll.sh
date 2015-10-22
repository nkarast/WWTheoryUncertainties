 #!/bin/bash

#Getting gcc 4.8.1

source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/x86_64/Gcc/gcc481_x86_64_slc6/setup.sh

#source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/x86_64/python/2.7.4-x86_64-slc6-gcc48/setup.sh

export BLAS=~/src/BLAS/libfblas.a
export LAPACK=~/src/lapack-*/libflapack.a


export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
  . ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
  . ${ATLAS_LOCAL_ROOT_BASE}/packageSetups/atlasLocalROOTSetup.sh --rootVersion=5.34.19-x86_64-slc6-gcc4.8
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(readlink -f shlib):$ROOTSYS/lib
  export PATH=$PATH:$ROOTSYS/bin

export PATH=$HOME/.local/bin:$PATH
export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH

export PATH=$HOME/bin/bin:$PATH
export LD_LIBRARY_PATH=$HOME/bin/lib:$LD_LIBRARY_PATH

export LD_LIBRARY_PATH=$HOME/src:$LD_LIBRARY_PATH
