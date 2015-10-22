#
#   @ author : Nikos Karastathis < nkarast .at. cern .dot. ch >
#
#   @ Loop over files and run bdt on thory ntuples
#


import os

workdir = os.getcwd()+'/rundir/'
filedir = '/glusterfs/atlas2/users/nikosk/TheoryNtuples/ueps/'

# for debugging purposes I am running only for the amcatnlo/nominal ones. Go up to TheoryNtuples/ueps/ in the 
# path below to run for all ntuples
for dirpath, subdirs, files in os.walk('/glusterfs/atlas2/users/nikosk/TheoryNtuples/ueps/amcatnlo/nominal/'):
    count = 0
    for f in files:
        count=count+1
        fname = os.path.join(dirpath,f)
        # NOW `name` can be the INPUT variable
        #print "["+ str(count)+ "] : " + name
        INPUT = fname
        BDT   = 'bdt'
        NJET  = '0jet'
        # AT THE MOMENT ONLY DO KHWW TRAINING
        #XMLFILE_EVEN = '/glusterfs/atlas2/users/nikosk/spin-ueps/bdt/weights/weights_BDT_4var_spin2pminvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_traineven_H125_0jet_emu/TMVAClassification_BDT_4var_spin2pminvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_traineven_H125_0jet_emu_BDT3.weights.xml'
	XMLFILE_EVEN = '/glusterfs/atlas2/users/nikosk/spin-ueps/bdt/weights/weights_BDT_CPEfun_spin0pv0m_allinputs_ptllmll_v00-02-31_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_traineven_H125_0jet_emu/TMVAClassification_BDT_CPEfun_spin0pv0m_allinputs_ptllmll_v00-02-31_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_traineven_H125_0jet_emu_BDT3.weights.xml'

        #XMLFILE_ODD =  '/glusterfs/atlas2/users/nikosk/spin-ueps/bdt/weights/weights_BDT_4var_spin2pminvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_trainodd_H125_0jet_emu/TMVAClassification_BDT_4var_spin2pminvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_trainodd_H125_0jet_emu_BDT3.weights.xml'
	XMLFILE_ODD ='/glusterfs/atlas2/users/nikosk/spin-ueps/bdt/weights/weights_BDT_CPEfun_spin0pv0m_allinputs_ptllmll_v00-02-31_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_trainodd_H125_0jet_emu/TMVAClassification_BDT_CPEfun_spin0pv0m_allinputs_ptllmll_v00-02-31_lead22sublead15_trackmet20_20_btag85_dphillCut_njet_trainodd_H125_0jet_emu_BDT3.weights.xml'

        
        CUTS_EVEN="'(Entry$ % 2 == 1)'"
        CUTS_ODD="'(Entry$ % 2 == 0)'"
        

        ALIASES= '/glusterfs/atlas2/users/nikosk/spin-ueps/bdt/aliases.py'
        TREENAME = 'tree'
        BDT_NAME_EVEN = 'bdt_nikos_kAWW_v31_0jet_2_1' #'bdt_spin_4var_2pmin_'+NJET+'_2_1'
        BDT_NAME_ODD =  'bdt_nikos_kAWW_v31_0jet_2_0'#'bdt_spin_4var_2pmin_'+NJET+'_2_0'
        
        command_even = 'python /glusterfs/atlas2/users/nikosk/spin-ueps/bdt/addbdt.py -f -i '+INPUT+' -t '+TREENAME+' -n '+BDT_NAME_EVEN+' -x '+XMLFILE_EVEN+' -c '+CUTS_EVEN+' -a '+ALIASES
        command_odd = 'python /glusterfs/atlas2/users/nikosk/spin-ueps/bdt/addbdt.py -f -i '+INPUT+' -t '+TREENAME+' -n '+BDT_NAME_ODD+' -x '+XMLFILE_ODD+' -c '+CUTS_ODD+' -a '+ALIASES
        print 'DEBUG : Running for file : ' + INPUT + ' for Even Weights.'
        #print command
        os.system(command_even)
        print 'DEBUG : Running for file : ' + INPUT + ' for Odd Weights.'
        os.system(command_odd)
        
    print 'DEBUG : Updating theory ntuples done %s files.' % str(count)

        

###### end of script -- ignore the statements below - left for debugging
