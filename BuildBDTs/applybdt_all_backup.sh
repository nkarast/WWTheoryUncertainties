#!/bin/sh

#PBS -r n
#PBS -e $HOME/pbs/log/job_${PBS_JOBID}.err
#PBS -o $HOME/pbs/log/job_${PBS_JOBID}.log
#PBS -q medium

set -v

export rundir=$( mktemp -d /tmp/tmp.XXXXXX )
cd ${rundir}

echo "running on $(hostname) @ $(date) in ${PWD} ..."

### ADD AN export INPUT = /path/to/file statement:
#
# Doug : 
# i typically run it in a for loop with qsub
# for file in $( find /path/to/ueps/files -name *_mod.root ); do export INPUT=${file}; qsub -v INPUT apply_bdtall.sh; done
# or the equivalent for lxbatch whatever that shit is



echo ${INPUT}

# cp -rvf ${INPUT} ${INPUT//.root/_mod.root}
# INPUT=${INPUT//.root/_mod.root}
# echo ${INPUT}

BDT="bdt" 

set +v

source $WORK/public/spin-ueps/bdt/myroot.sh

set -v

if [ "x${SKIPDONE}" == "x" ]; then
    SKIPDONE=yes
fi

if [ "x${NJET}" == "x" ]; then
    NJET="0jet"
fi 

if [ "x${TREE}" == "x" ]; then
    TREE="tree"
fi

# doSPIN=yes
# doCP=yes

######################################################################
############################### SPIN #################################
######################################################################

if [ "x${doSPIN}" == "xyes" ]; then

    BDT="bdt_spin_4var" 
    # 0p
    if [ $( root -l -q -b "$HOME/public/spin-ueps/bdt/checktree.C(\"${INPUT}\", \"${BDT}_${NJET}_0_1)" 2>&1 | grep -c ERROR ) -ne 0 -o "x${SKIPDONE}" != "xyes" ]; then

	$HOME/public/spin-ueps/bdt/addbdt.py -f -i ${INPUT} -t $TREE -n ${BDT}_${NJET}_0_1 \
	    -x $HOME/public/spin-ueps/bdt/weights/weights_BDT_4var_spin0pvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_10_btag85_dphillCut_njet_traineven_H125_${NJET}_emu/TMVAClassification_BDT_4var_spin0pvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_10_btag85_dphillCut_njet_traineven_H125_${NJET}_emu_BDT3.weights.xml \
	    -c '(Entry$ % 2 == 1)' -a $HOME/public/spin-ueps/bdt/aliases.py 2>&1 | grep -v "Error in <TSystem::ExpandFileName>"

    fi

    if [ $( root -l -q -b "$HOME/public/spin-ueps/bdt/checktree.C(\"${INPUT}\", \"${BDT}_${NJET}_0_0)" 2>&1 | grep -c ERROR ) -ne 0 -o "x${SKIPDONE}" != "xyes" ]; then

	$HOME/public/spin-ueps/bdt/addbdt.py -f -i ${INPUT} -t $TREE -n ${BDT}_${NJET}_0_0 \
	    -x $HOME/public/spin-ueps/bdt/weights/weights_BDT_4var_spin0pvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_10_btag85_dphillCut_njet_trainodd_H125_${NJET}_emu/TMVAClassification_BDT_4var_spin0pvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_10_btag85_dphillCut_njet_trainodd_H125_${NJET}_emu_BDT3.weights.xml \
	    -c '(Entry$ % 2 == 0)' -a $HOME/public/spin-ueps/bdt/aliases.py 2>&1 | grep -v "Error in <TSystem::ExpandFileName>"
    fi

    ## 2p
    if [ $( root -l -q -b "$HOME/public/spin-ueps/bdt/checktree.C(\"${INPUT}\", \"${BDT}_2p_${NJET}_2_1)" 2>&1 | grep -c ERROR ) -ne 0 -o "x${SKIPDONE}" != "xyes" ]; then

	$HOME/public/spin-ueps/bdt/addbdt.py -f -i ${INPUT} -t $TREE -n ${BDT}_2p_${NJET}_2_1 \
	    -x $HOME/public/spin-ueps/bdt/weights/weights_BDT_4var_spin2pvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_10_btag85_dphillCut_njet_traineven_H125_${NJET}_emu/TMVAClassification_BDT_4var_spin2pvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_10_btag85_dphillCut_njet_traineven_H125_${NJET}_emu_BDT3.weights.xml \
	    -c '(Entry$ % 2 == 1)' -a $HOME/public/spin-ueps/bdt/aliases.py 2>&1 | grep -v "Error in <TSystem::ExpandFileName>"
    fi

    if [ $( root -l -q -b "$HOME/public/spin-ueps/bdt/checktree.C(\"${INPUT}\", \"${BDT}_2p_${NJET}_2_0)" 2>&1 | grep -c ERROR ) -ne 0 -o "x${SKIPDONE}" != "xyes" ]; then

	$HOME/public/spin-ueps/bdt/addbdt.py -f -i ${INPUT} -t $TREE -n ${BDT}_2p_${NJET}_2_0 \
	    -x $HOME/public/spin-ueps/bdt/weights/weights_BDT_4var_spin2pvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_10_btag85_dphillCut_njet_trainodd_H125_${NJET}_emu/TMVAClassification_BDT_4var_spin2pvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_10_btag85_dphillCut_njet_trainodd_H125_${NJET}_emu_BDT3.weights.xml \
	    -c '(Entry$ % 2 == 0)' -a $HOME/public/spin-ueps/bdt/aliases.py 2>&1 | grep -v "Error in <TSystem::ExpandFileName>"

    fi

    ## 2pmin
    if [ $( root -l -q -b "$HOME/public/spin-ueps/bdt/checktree.C(\"${INPUT}\", \"${BDT}_2pmin_${NJET}_2_1)" 2>&1 | grep -c ERROR ) -ne 0 -o "x${SKIPDONE}" != "xyes" ]; then

	$HOME/public/spin-ueps/bdt/addbdt.py -f -i ${INPUT} -t $TREE -n ${BDT}_2pmin_${NJET}_2_1 \
	    -x $HOME/public/spin-ueps/bdt/weights/weights_BDT_4var_spin2pminvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_traineven_H125_${NJET}_emu/TMVAClassification_BDT_4var_spin2pminvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_traineven_H125_${NJET}_emu_BDT3.weights.xml \
	    -c '(Entry$ % 2 == 1)' -a $HOME/public/spin-ueps/bdt/aliases.py 2>&1 | grep -v "Error in <TSystem::ExpandFileName>"
    fi

    if [ $( root -l -q -b "$HOME/public/spin-ueps/bdt/checktree.C(\"${INPUT}\", \"${BDT}_2pmin_${NJET}_2_0)" 2>&1 | grep -c ERROR ) -ne 0 -o "x${SKIPDONE}" != "xyes" ]; then

	$HOME/public/spin-ueps/bdt/addbdt.py -f -i ${INPUT} -t $TREE -n ${BDT}_2pmin_${NJET}_2_0 \
	    -x $HOME/public/spin-ueps/bdt/weights/weights_BDT_4var_spin2pminvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_trainodd_H125_${NJET}_emu/TMVAClassification_BDT_4var_spin2pminvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_trainodd_H125_${NJET}_emu_BDT3.weights.xml \
	    -c '(Entry$ % 2 == 0)' -a $HOME/public/spin-ueps/bdt/aliases.py 2>&1 | grep -v "Error in <TSystem::ExpandFileName>"

    fi

    ## 2pkg05kq1
    if [ $( root -l -q -b "$HOME/public/spin-ueps/bdt/checktree.C(\"${INPUT}\", \"${BDT}_2pkg05kq1_${NJET}_2_1)" 2>&1 | grep -c ERROR ) -ne 0 -o "x${SKIPDONE}" != "xyes" ]; then

	$HOME/public/spin-ueps/bdt/addbdt.py -f -i ${INPUT} -t $TREE -n ${BDT}_2pkg05kq1_${NJET}_2_1 \
	    -x $HOME/public/spin-ueps/bdt/weights/weights_BDT_4var_spin2pkg05kq1vBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_HPt125_traineven_H125_${NJET}_emu/TMVAClassification_BDT_4var_spin2pkg05kq1vBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_HPt125_traineven_H125_${NJET}_emu_BDT3.weights.xml \
	    -c '(Entry$ % 2 == 1)' -a $HOME/public/spin-ueps/bdt/aliases.py 2>&1 | grep -v "Error in <TSystem::ExpandFileName>"
    fi

    if [ $( root -l -q -b "$HOME/public/spin-ueps/bdt/checktree.C(\"${INPUT}\", \"${BDT}_2pkg05kq1_${NJET}_2_0)" 2>&1 | grep -c ERROR ) -ne 0 -o "x${SKIPDONE}" != "xyes" ]; then

	$HOME/public/spin-ueps/bdt/addbdt.py -f -i ${INPUT} -t $TREE -n ${BDT}_2pkg05kq1_${NJET}_2_0 \
	    -x $HOME/public/spin-ueps/bdt/weights/weights_BDT_4var_spin2pkg05kq1vBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_HPt125_trainodd_H125_${NJET}_emu/TMVAClassification_BDT_4var_spin2pkg05kq1vBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_HPt125_trainodd_H125_${NJET}_emu_BDT3.weights.xml \
	    -c '(Entry$ % 2 == 0)' -a $HOME/public/spin-ueps/bdt/aliases.py 2>&1 | grep -v "Error in <TSystem::ExpandFileName>"

    fi

    ## 2pkg1kq0
    if [ $( root -l -q -b "$HOME/public/spin-ueps/bdt/checktree.C(\"${INPUT}\", \"${BDT}_2pkg1kq0_${NJET}_2_1)" 2>&1 | grep -c ERROR ) -ne 0 -o "x${SKIPDONE}" != "xyes" ]; then

	$HOME/public/spin-ueps/bdt/addbdt.py -f -i ${INPUT} -t $TREE -n ${BDT}_2pkg1kq0_${NJET}_2_1 \
	    -x $HOME/public/spin-ueps/bdt/weights/weights_BDT_4var_spin2pkg1kq0vBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_HPt125_traineven_H125_${NJET}_emu/TMVAClassification_BDT_4var_spin2pkg1kq0vBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_HPt125_traineven_H125_${NJET}_emu_BDT3.weights.xml \
	    -c '(Entry$ % 2 == 1)' -a $HOME/public/spin-ueps/bdt/aliases.py 2>&1 | grep -v "Error in <TSystem::ExpandFileName>"
    fi

    if [ $( root -l -q -b "$HOME/public/spin-ueps/bdt/checktree.C(\"${INPUT}\", \"${BDT}_2pkg1kq0_${NJET}_2_0)" 2>&1 | grep -c ERROR ) -ne 0 -o "x${SKIPDONE}" != "xyes" ]; then

	$HOME/public/spin-ueps/bdt/addbdt.py -f -i ${INPUT} -t $TREE -n ${BDT}_2pkg1kq0_${NJET}_2_0 \
	    -x $HOME/public/spin-ueps/bdt/weights/weights_BDT_4var_spin2pkg1kq0vBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_HPt125_trainodd_H125_${NJET}_emu/TMVAClassification_BDT_4var_spin2pkg1kq0vBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_HPt125_trainodd_H125_${NJET}_emu_BDT3.weights.xml \
	    -c '(Entry$ % 2 == 0)' -a $HOME/public/spin-ueps/bdt/aliases.py 2>&1 | grep -v "Error in <TSystem::ExpandFileName>"

    fi
fi

######################################################################
################################# CP #################################
######################################################################

if [ "x${doCP}" == "xyes" ]; then
    
    BDT="bdt_cp" 

    if [ $( root -l -q -b "$HOME/public/spin-ueps/bdt/checktree.C(\"${INPUT}\", \"${BDT}_CPE_1)" 2>&1 | grep -c ERROR ) -ne 0 -o "x${SKIPDONE}" != "xyes" ]; then

	$HOME/public/spin-ueps/bdt/addbdt.py -f -i ${INPUT} -t $TREE -n ${BDT}_CPE_1 \
	    -x $HOME/public/spin-ueps/bdt/weights/weights_BDT_CPEfun_spin0pv0m_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_traineven_H125_0jet_emu/TMVAClassification_BDT_CPEfun_spin0pv0m_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_traineven_H125_0jet_emu_BDT3.weights.xml \
	    -c '(Entry$ % 2 == 1)' -a $HOME/public/spin-ueps/bdt/aliases.py 2>&1 | grep -v "Error in <TSystem::ExpandFileName>"

    fi

    if [ $( root -l -q -b "$HOME/public/spin-ueps/bdt/checktree.C(\"${INPUT}\", \"${BDT}_CPE_0)" 2>&1 | grep -c ERROR ) -ne 0 -o "x${SKIPDONE}" != "xyes" ]; then

	$HOME/public/spin-ueps/bdt/addbdt.py -f -i ${INPUT} -t $TREE -n ${BDT}_CPE_0 \
	    -x $HOME/public/spin-ueps/bdt/weights/weights_BDT_CPEfun_spin0pv0m_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_trainodd_H125_0jet_emu/TMVAClassification_BDT_CPEfun_spin0pv0m_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_trainodd_H125_0jet_emu_BDT3.weights.xml \
	    -c '(Entry$ % 2 == 0)' -a $HOME/public/spin-ueps/bdt/aliases.py 2>&1 | grep -v "Error in <TSystem::ExpandFileName>"
    fi


    if [ $( root -l -q -b "$HOME/public/spin-ueps/bdt/checktree.C(\"${INPUT}\", \"${BDT}_kHWW_1)" 2>&1 | grep -c ERROR ) -ne 0 -o "x${SKIPDONE}" != "xyes" ]; then

	$HOME/public/spin-ueps/bdt/addbdt.py -f -i ${INPUT} -t $TREE -n ${BDT}_kHWW_1 \
	    -x $HOME/public/spin-ueps/bdt/weights/weights_BDT_kHWWScan_spin0pvkHWW_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_traineven_H125_0jet_emu/TMVAClassification_BDT_kHWWScan_spin0pvkHWW_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_traineven_H125_0jet_emu_BDT3.weights.xml \
	    -c '(Entry$ % 2 == 1)' -a $HOME/public/spin-ueps/bdt/aliases.py 2>&1 | grep -v "Error in <TSystem::ExpandFileName>"

    fi

    if [ $( root -l -q -b "$HOME/public/spin-ueps/bdt/checktree.C(\"${INPUT}\", \"${BDT}_kHWW_0)" 2>&1 | grep -c ERROR ) -ne 0 -o "x${SKIPDONE}" != "xyes" ]; then

	$HOME/public/spin-ueps/bdt/addbdt.py -f -i ${INPUT} -t $TREE -n ${BDT}_kHWW_0 \
	    -x  $HOME/public/spin-ueps/bdt/weights/weights_BDT_kHWWScan_spin0pvkHWW_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_trainodd_H125_0jet_emu/TMVAClassification_BDT_kHWWScan_spin0pvkHWW_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_trainodd_H125_0jet_emu_BDT3.weights.xml \
	    -c '(Entry$ % 2 == 0)' -a $HOME/public/spin-ueps/bdt/aliases.py 2>&1 | grep -v "Error in <TSystem::ExpandFileName>"
    fi
fi

######################################################################
######################################################################
######################################################################

set +v

cd /tmp

rm -rf ${rundir}
