#!/bin/bash

#PBS -r n
#PBS -e $HOME/pbs/log/job_${PBS_JOBID}.err
#PBS -o $HOME/pbs/log/job_${PBS_JOBID}.log
#PBS -q medium

#set -v

#export rundir=$( mktemp -d /tmp/nkarast/tmp.XXXXXX )
export rundir=${PWD}/rundir/
cd ${rundir}

#echo "running on $(hostname) @ $(date) in ${PWD} ..."

### ADD AN export INPUT = /path/to/file statement:
#
# Doug : 
# i typically run it in a for loop with qsub
# for file in $( find /path/to/ueps/files -name *_mod.root ); do export INPUT=${file}; qsub -v INPUT apply_bdtall.sh; done
# or the equivalent for lxbatch whatever that shit is



#echo ${INPUT}

# cp -rvf ${INPUT} ${INPUT//.root/_mod.root}
# INPUT=${INPUT//.root/_mod.root}
# echo ${INPUT}

BDT="bdt" 

#set +v

#source ${PWD}/myroot.sh

#set -v

if [ "x${SKIPDONE}" == "x" ]; then
    SKIPDONE=yes
fi

if [ "x${NJET}" == "x" ]; then
    NJET="0jet"
fi 

if [ "x${TREE}" == "x" ]; then
    TREE="tree"
fi

 doSPIN=yes


if [ "x${doSPIN}" == "xyes" ]; then

    BDT="bdt_spin_4var"

#echo  root -l -q -b '/glusterfs/atlas2/users/nikosk/spin-ueps/bdt/checktree.C('${INPUT}','${BDT}'_2pkg05kq1_hpt300_test_'${NJET}'_2_1)'
  if [ $(root -l -q -b "\/glusterfs\/atlas2\/users\/nikosk\/spin-ueps\/bdt\/checktree.C\("${INPUT}\"\, \"${BDT}"_2pkg05kq1_hpt300_test_"${NJET}"_2_1)" 2>&1 | grep -c ERROR ) -ne 0 -o "x${SKIPDONE}" != "xyes" ]; then

       python /glusterfs/atlas2/users/nikosk/spin-ueps/bdt/addbdt.py -f -i ${INPUT} -t $TREE -n ${BDT}_2pkg05kq1_hpt300_test_${NJET}_2_1 \
	    -x /glusterfs/atlas2/users/nikosk/spin-ueps/bdt/weights/weights_BDT_4var_spin2pkg05kq1vBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_HPt300_traineven_H125_${NJET}_emu/TMVAClassification_BDT_4var_spin2pkg05kq1vBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_HPt300_traineven_H125_${NJET}_emu_BDT3.weights.xml \
	    -c '(Entry$ % 2 == 1)' -a /glusterfs/atlas2/users/nikosk/spin-ueps/bdt/aliases.py 2>&1 | grep -v "Error in <TSystem::ExpandFileName>"
    fi
fi