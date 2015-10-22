import ROOT as rt
import glob
import os
import math

# debug switch
debug = 1

#
# the directory where the temp files are kept
#
rundir = "./histfiles/py6_hists/"

#
# loop over all files under the ./ directory whose name matches the pattern `ww*_mod.root`
#
filecounter = 0
for f in glob.glob("/glusterfs/atlas2/users/nikosk/TheoryNtuples/ueps/py6_me/ww*_mod.root"):    #set the input directory properly (glob.glob is used to make expressions matching)
    if debug : print "DEBUG from makeSelection: Working on file", f
    ifile = rt.TFile.Open(f,"read")
    kintree = ifile.Get("tree")
    mvatree = ifile.Get("MVA")

    kintree_entries = kintree.GetEntriesFast()
    mvatree_entries = mvatree.GetEntries()

    if debug : print "DEBUG from makeSelection: Entries of",f," (tree,MVA):(",kintree_entries, ",", mvatree_entries,")"


    # define the histograms for the 1D bdt distributions , we need 8 of them
    h1_spin0p_bdt = rt.TH1F("bdt_spin0p_0jet","bdt_spin0p_0jet", 25, -1, 1)
    
    h1_spin2pmin_bdt = rt.TH1F("bdt_spin2pmin_0jet", "bdt_spin2pmin_0jet", 25, -1,1)

    h1_spin2pkg05kq1_hpt125_bdt = rt.TH1F("bdt_spin2pkg05kq1_hpt125_0jet", "bdt_spin2pkg05kq1_hpt125_0jet", 25, -1,1)
    h1_spin2pkg05kq1_hpt300_bdt = rt.TH1F("bdt_spin2pkg05kq1_hpt300_0jet", "bdt_spin2pkg05kq1_hpt300_0jet", 25, -1,1)
    
    h1_spin2pkg1kq0_hpt125_bdt = rt.TH1F("bdt_spin2pkg1kq0_hpt125_0jet", "bdt_spin2pkg1kq0_hpt125_0jet", 25, -1, 1)
    h1_spin2pkg1kq0_hpt300_bdt = rt.TH1F("bdt_spin2pkg1kq0_hpt300_0jet", "bdt_spin2pkg1kq0_hpt300_0jet", 25, -1, 1)
    
    h1_kAWW_bdt = rt.TH1F("bdt_kAWW_0jet", "bdt_kAWW_0jet", 25, -1, 1)
    h1_kHWW_bdt = rt.TH1F("bdt_kHWW_0jet", "bdt_kHWW_0jet", 25, -1, 1)

    # define the histograms for the 2D bdt distributions - we need all 7 of them vs the spin0p one
    # ------- spin0 vs spin2_x for 0jet are 10x5 histos:
    h2_spin0p_spin2pmin_bdt = rt.TH2F("bdt2_spin0p_spin2pmin_0jet", "bdt2_spin0p_spin2pmin_0jet", 10, -1, 1, 5, -1, 1)

    h2_spin0p_spin2pkg05kq1_hpt125_bdt = rt.TH2F("bdt_spin0p_spin2pkg05kq1_hpt125_0jet", "bdt_spin0p_spin2pkg05kq1_hpt125_0jet",10, -1, 1, 5, -1, 1)
    h2_spin0p_spin2pkg05kq1_hpt300_bdt = rt.TH2F("bdt_spin0p_spin2pkg05kq1_hpt300_0jet", "bdt_spin0p_spin2pkg05kq1_hpt300_0jet",10, -1, 1, 5, -1, 1)
    
    h2_spin0p_spin2pkg1kq0_hpt125_bdt = rt.TH2F("bdt_spin0p_spin2pkg1kq0_hpt125_0jet","bdt_spin0p_spin2pkg1kq0_hpt125_0jet",10, -1, 1, 5, -1, 1)
    h2_spin0p_spin2pkg1kq0_hpt300_bdt = rt.TH2F("bdt_spin0p_spin2pkg1kq0_hpt300_0jet","bdt_spin0p_spin2pkg1kq0_hpt300_0jet",10, -1, 1, 5, -1, 1)
    
    # ------- spin0 vs spin0_x for 0jet are 5x15 histos:
    h2_spin0p_kAWW_bdt = rt.TH2F("bdt_spin0p_kAWW_0jet", "bdt_spin0p_kAWW_0jet", 5,-1,1,15,-1,1)
    h2_spin0p_kHWW_bdt = rt.TH2F("bdt_spin0p_kHWW_0jet", "bdt_spin0p_kHWW_0jet", 5,-1,1,15,-1,1)
    

    number_good_events = 0
    for event in ifile.tree:
        good_event = True
        if event.lep1_pdgId == event.lep2_pdgId: good_event = False
        if event.mll<10. : good_event = False
        if event.jet_n!=0 : good_event = False
        if event.ptll<20. : good_event = False
        if event.mll>80. : good_event = False
        if math.fabs(event.phill)>2.8 : good_event = False
        if event.met <20. : good_event = False
        if not (max(event.lep1_pt,event.lep2_pt)>22. and min(event.lep1_pt, event.lep2_pt)>15) : good_event = False
    
        if good_event:
            number_good_events = number_good_events+1
            
            # fill 1D distributions
            h1_spin0p_bdt.Fill(max(event.bdt_spin_4var_0jet_0_0, event.bdt_spin_4var_0jet_0_1))
            
            h1_spin2pmin_bdt.Fill(max(event.bdt_spin_4var_2pmin_0jet_2_0,event.bdt_spin_4var_2pmin_0jet_2_1))
            
            h1_spin2pkg05kq1_hpt125_bdt.Fill(max(event.bdt_spin_4var_2pkg05kq1_0jet_2_0,event.bdt_spin_4var_2pkg05kq1_0jet_2_1))
            h1_spin2pkg05kq1_hpt300_bdt.Fill(max(event.bdt_spin_4var_2pkg05kq1_0jet_2_0,event.bdt_spin_4var_2pkg05kq1_0jet_2_1))
            
            h1_spin2pkg1kq0_hpt125_bdt.Fill(max(event.bdt_spin_4var_2pkg1kq0_0jet_2_0, event.bdt_spin_4var_2pkg1kq0_0jet_2_1 ))
            h1_spin2pkg1kq0_hpt300_bdt.Fill(max(event.bdt_spin_4var_2pkg1kq0_0jet_2_0, event.bdt_spin_4var_2pkg1kq0_0jet_2_1 ))
            
            h1_kAWW_bdt.Fill(max(event.bdt_nikos_kAWW_v31_0jet_2_0, event.bdt_nikos_kAWW_v31_0jet_2_1))
            h1_kHWW_bdt.Fill(max(event.bdt_nikos_kHWW_v31_0jet_2_0, event.bdt_nikos_kHWW_v31_0jet_2_1))
            
            
            # fill 2D distributions
            
            h2_spin0p_spin2pmin_bdt.Fill(max(event.bdt_spin_4var_0jet_0_0, event.bdt_spin_4var_0jet_0_1),max(event.bdt_spin_4var_2pmin_0jet_2_0,event.bdt_spin_4var_2pmin_0jet_2_1))
            
            h2_spin0p_spin2pkg05kq1_hpt125_bdt.Fill(max(event.bdt_spin_4var_0jet_0_0, event.bdt_spin_4var_0jet_0_1),max(event.bdt_spin_4var_2pkg05kq1_0jet_2_0,event.bdt_spin_4var_2pkg05kq1_0jet_2_1))
            h2_spin0p_spin2pkg05kq1_hpt300_bdt.Fill(max(event.bdt_spin_4var_0jet_0_0, event.bdt_spin_4var_0jet_0_1),max(event.bdt_spin_4var_2pkg05kq1_0jet_2_0,event.bdt_spin_4var_2pkg05kq1_0jet_2_1))
            
            h2_spin0p_spin2pkg1kq0_hpt125_bdt.Fill(max(event.bdt_spin_4var_0jet_0_0, event.bdt_spin_4var_0jet_0_1),max(event.bdt_spin_4var_2pkg1kq0_0jet_2_0, event.bdt_spin_4var_2pkg1kq0_0jet_2_1 ))
            h2_spin0p_spin2pkg1kq0_hpt300_bdt.Fill(max(event.bdt_spin_4var_0jet_0_0, event.bdt_spin_4var_0jet_0_1),max(event.bdt_spin_4var_2pkg1kq0_0jet_2_0, event.bdt_spin_4var_2pkg1kq0_0jet_2_1 ))
            
            h2_spin0p_kAWW_bdt.Fill(max(event.bdt_spin_4var_0jet_0_0, event.bdt_spin_4var_0jet_0_1),max(event.bdt_nikos_kAWW_v31_0jet_2_0, event.bdt_nikos_kAWW_v31_0jet_2_1))
            h2_spin0p_kHWW_bdt.Fill(max(event.bdt_spin_4var_0jet_0_0, event.bdt_spin_4var_0jet_0_1),max(event.bdt_nikos_kHWW_v31_0jet_2_0, event.bdt_nikos_kHWW_v31_0jet_2_1))
            
            
            ## -- old stuff:
            #h_bdt_0.Fill(max(event.bdt_spin_4var_0jet_0_1, event.bdt_spin_4var_0jet_0_0))
            #h_bdt_2.Fill(max(event.bdt_nikos_kAWW_v31_0jet_2_0,event.bdt_nikos_kAWW_v31_0jet_2_1))
            #h2_bdt.Fill(max(event.bdt_spin_4var_0jet_0_1, event.bdt_spin_4var_0jet_0_0),max(event.bdt_nikos_kAWW_v31_0jet_2_0,event.bdt_nikos_kAWW_v31_0jet_2_1))
        else: continue

    if debug : print "DEBUG from makeselection: Selection kept [",number_good_events,"/",kintree_entries,"]"

    # the outfile name has a tag and a counter
    outname = rundir+"outputHists_py6_"+str(filecounter)+".root"
    outfile = rt.TFile.Open(outname, "recreate")
    outfile.cd()
    h1_spin0p_bdt.Write()
    h1_spin2pmin_bdt.Write()
    h1_spin2pkg05kq1_hpt125_bdt.Write()
    h1_spin2pkg05kq1_hpt300_bdt.Write()
    h1_spin2pkg1kq0_hpt125_bdt.Write()
    h1_spin2pkg1kq0_hpt300_bdt.Write()
    h1_kAWW_bdt.Write()
    h1_kHWW_bdt.Write()
    
    h2_spin0p_spin2pmin_bdt.Write()
    h2_spin0p_spin2pkg05kq1_hpt125_bdt.Write()
    h2_spin0p_spin2pkg05kq1_hpt300_bdt.Write()
    h2_spin0p_spin2pkg1kq0_hpt125_bdt.Write()
    h2_spin0p_spin2pkg1kq0_hpt300_bdt.Write()
    h2_spin0p_kAWW_bdt.Write()
    h2_spin0p_kHWW_bdt.Write()
    
    outfile.Close()
    ifile.Close()
    if debug : print "Debug from makeSelection: Wrote file",outname,"\n----"
    filecounter = filecounter+1


print ' DONE '

# add a hadd option -- remove the comment to also delete the temp files
#hadd_flag =  raw_input("Hadd output files? [y/n]\n")
#if hadd_flag=="y" or hadd_flag=="yes" or hadd_flag =="Yes" or hadd_flag=="YES":
#    mergecommand = "hadd -f py6_2dbdt.root outputHists_py6_*"
#    cdcommand = "cd "+rundir
#    os.system(cdcommand)
#    os.system(mergecommand)
#    #os.system("rm -rf outputHists_amcatnlo_*")   # uncomment to also remove the intermediate files
