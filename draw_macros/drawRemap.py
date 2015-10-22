import ROOT as rt
import math


# option flags
debug = 1
do_plot = 0
do_full_log = 0
write_file  = 0

############################################################################
#
#   functions to use later
#
############################################################################
#   Get a list with the remap bins (1st column of cfg file)
#       - cfg file : a string to the cfg file
#   Returns : a list object
def get_remap_config(cfgfile):
    incfgfile = open(cfgfile,'r')
    remapList = []
    for line in incfgfile.readlines():
        print line.split()
        if "#" in line[0] or line[0]=="" or ":" in line[0] or line[0]=='\n': continue
        else: remapList.append(int(line[0]))
    if debug : print "Remap list is : ",remapList
    incfgfile.close()
    print "INFO: Reading cfg file [",incfgfile,"]... DONE"
    return remapList


#   Get the unrolled 2D histogram:
#       - infile : string to the input ROOT file that contains the 2D hist
#       - histname : name of the histogram in the file
#       - tag : tag to put in the name of the unrolled (amcatnlo or powheg)
#   Returns : a TH1F object with 50 bins from -1 to 1

def get_unrolled(infile, histname,tag):
    ifile = rt.TFile.Open(infile,"read")
    h2_bdt = ifile.Get(histname)
    h2_bdt.Sumw2()
    #        h2_bdt = ifile.Get("MVAOutput0_MVAOutput2_20bins_0jet_emu_all")
    name = tag+"_unrolled"
    nxbins = h2_bdt.GetNbinsX()
    nybins = h2_bdt.GetNbinsY()
    tot_bins = nxbins*nybins
    if debug : print ' DEBUG from get_unrolled : (xbins,ybins,total) = (',nxbins,',',nybins,',',tot_bins,')'
    h1_unrolled = rt.TH1F(name,name,tot_bins,-1   ,1)
    h1_unrolled.Sumw2()
    binI=0
    for x_bin in range(1,nxbins+1):
        for y_bin in range(1,nybins+1):
            binI=binI+1
            bin_sig0 = h2_bdt.GetBinContent(x_bin,y_bin)
            bin_sig0_err = h2_bdt.GetBinError(x_bin,y_bin)
            h1_unrolled.SetBinContent(binI,bin_sig0)
            h1_unrolled.SetBinError(binI, bin_sig0_err)
    print "INFO: Unrolling",tag,"... DONE"
    if debug : print ' DEBUG from get_unrolled : final unrolled histo has = (', h1_unrolled.GetNbinsX(), ' bins )'
    return h1_unrolled


#   Get the remapped distribution, named "remapped_"+tag:
#       - remapList : a list containing the remapped bins (use get_remap_config function)
#       - h_unrolled : a histogram with the unrolled distribution (use get_unrolled)
#       - tag : tag to put in the name of the unrolled (amcatnlo or powheg)
#   Returns : a TH1F object with len(remapList) bins from -1 to 1
def get_remappedBDT(remapList,h_unrolled, tag):
    name = "remapped_"+tag
    h1_remapped = rt.TH1F(name,name,len(remapList),-1,1)
    h1_remapped.Sumw2()
    
    bin_in =  1
    for i in range(len(remapList)):
        #     if debug: print "iteration:",i
        bin_out = i+1
        content = 0.
        sumerror2 = 0
        for j in range(remapList[i]):
            #   if debug: print "for item in list =",remapList[i],"iteration:",j, " with bin in",bin_in, "and bin out", bin_out
            content = content+h_unrolled.GetBinContent(bin_in)
            # if debug: print "content = ", content
            error = h_unrolled.GetBinError(bin_in)
            error2 = error*error
            sumerror2 = sumerror2+error2
            bin_in = bin_in+1
        h1_remapped.SetBinContent(bin_out,content)
        h1_remapped.SetBinError(bin_out,math.sqrt(sumerror2))
    #if debug: print content, sumerror2
    print "INFO: Remapping",tag,"... DONE"
    return h1_remapped





############################################################################
#
#   main block of code
#
############################################################################

# STEP 1 ) GET THE REMAP LIST (READ CFG)
remapList = get_remap_config("cfg/Spin0m_0j_5x15_v31.cfg")    #### change the cfg file in


# STEP 2 ) GET THE UNROLLED DISTRIBUTIONS
py6_unroll = get_unrolled("histfiles/final_pythia6_0jet.root","bdt_spin0p_kAWW_0jet","py6")
amc_unroll = get_unrolled("histfiles/final_amcatnlo_0jet.root","bdt_spin0p_kAWW_0jet","amcatnlo")  #### carefull about jets and bdt
her_unroll = get_unrolled("histfiles/final_herwig_0jet.root","bdt_spin0p_kAWW_0jet","herwig")


canvas_unr = rt.TCanvas("unroll","unroll",800,600)
rt.gStyle.SetOptStat(0)
amc_unroll.SetLineColor(rt.kRed)
amc_unroll.SetLineWidth(2)
her_unroll.SetLineColor(rt.kBlue)
her_unroll.SetLineWidth(2)
amc_unroll.SetTitle("")
amc_unroll.GetXaxis().SetTitle("Unrolled")
leg_unroll = rt.TLegend(0.60, 0.70, 0.88, 0.86)
leg_unroll.SetBorderSize(0)
leg_unroll.SetTextFont(42)
leg_unroll.SetTextSize(0.032)
leg_unroll.SetFillColor(0)
leg_unroll.SetNColumns(1)
leg_unroll.AddEntry(amc_unroll, "amc@NLO", "lep")
leg_unroll.AddEntry(her_unroll, "Powheg", "lep")
amc_unroll.Scale(1/amc_unroll.Integral())
her_unroll.Scale(1/her_unroll.Integral())
amc_unroll.Draw("e")
her_unroll.Draw("e same")
leg_unroll.Draw("same")

canvas_unr.SaveAs("SomePlots/amc_powheg_kAWW_unrolled.pdf")


# STEP 3.a) GET THE REMAPPED DISTRIBUTIONS ACCORDING TO THE CFG FILE
py6_remap = get_remappedBDT(remapList, py6_unroll, "py6")
amc_remap = get_remappedBDT(remapList, amc_unroll, "amc")
her_remap = get_remappedBDT(remapList, her_unroll, "her")


# STEP 3.b) GET THE ENTRIES PER BIN FOR THE REMAPPED DISTRIBUTIONS
amc_remap_content=[]
her_remap_content=[]

for ibin in range(1, amc_remap.GetNbinsX()+1):
    amc_remap_content.append(amc_remap.GetBinContent(ibin))
    her_remap_content.append(her_remap.GetBinContent(ibin))


# STEP 4) NORMALIZE THE REMAPPED DISTRIBUTIONS
py6_remap.Scale(1/py6_remap.Integral())
amc_remap.Scale(1/amc_remap.Integral())
her_remap.Scale(1/her_remap.Integral())


# STEP 5.a) GET THE RATIO OF AMC-at-NLO over POWHEG
ratio = amc_remap.Clone()
ratio.Sumw2()
ratio.Divide(her_remap)


# STEP 5.b) GET THE CONTENT AND ERROR PER BIN FOR THE RATIO HISTOGRAM
content1 = []
error1 = []
for ibin in range(1, ratio.GetNbinsX()+1):
    content1.append(ratio.GetBinContent(ibin))
    error1.append(ratio.GetBinError(ibin))
# --- write full log with ratio, error and entries of the two files
if do_full_log:
    fullLog=open('fullLogs/spin2pkg1kq0_hpt300_1jet.dat','w')  #### change the name of the full log file
    fullLog.write('# ratio_content , ratio_error , amcatnlo_remap_content , powheg+herwig_remap_content\n')
    for i in range(len(content1)):
        fullLog.write('%0.10f\t%0.10f\t%f\t%f\n' % (math.fabs(1.-content1[i]), error1[i], amc_remap_content[i], her_remap_content[i]))
    print 'INFO : full log file written ',fullLog

# STEP 6) APPLY A CUT ON BINS WITH ERRORS > 0.01
new_content = []
for ibin in range(len(error1)):
    if error1[ibin]>0.01 :
        content1[ibin] = 1.0

final_content=[]
print '#--------------------------'
for i in range(len(content1)):
    final_content.append(math.fabs(1.-content1[i]))
    print math.fabs(1.-content1[i]) ,amc_remap_content[i]
# --- write output file
if write_file:
    outfile = open('outFiles/ww_model_spin2pkg1kq0_HPt300_1jet_v31.dat','w')  #### change the name of the file
    outfile.write('# ww model spin2pmin 0jet\n')
    for i in range(len(final_content)):
        outfile.write('%0.10f\n' % final_content[i])
    print 'INFO : outfile written ',outfile


# STEP6 : GET SOME HISTOS -- check the do_plot flag
if do_plot:
    h_nom = rt.TH1F("nominal_hist_spin2pmin_1j", "nominal_hist_spin2pmin_1j", ratio.GetNbinsX(), -1, 1)
    h_nom.Sumw2()
    h_up = rt.TH1F("up_hist_spin2pmin_1j", "up_hist_spin2pmin_1j", ratio.GetNbinsX(), -1, 1)
    h_up.Sumw2()
    h_dw = rt.TH1F("dw_hist_spin2pmin_1j", "dw_hist_spin2pmin_1j", ratio.GetNbinsX(), -1, 1)
    h_dw.Sumw2()

    for i in range(ratio.GetNbinsX()):
        h_nom.SetBinContent(i+1, 1)
        h_nom.SetBinError(i+1, ratio.GetBinError(i))

        h_up.SetBinContent(i+1, 1.+final_content[i])
        h_up.SetBinError(i+1, ratio.GetBinError(i))

        h_dw.SetBinContent(i+1, 1.-final_content[i])
        h_dw.SetBinError(i+1, ratio.GetBinError(i))




    h_nom.SetLineColor(rt.kBlack)
    h_up.SetLineColor(rt.kRed)
    #h_up.SetFillColor(rt.kRed)
    #h_up.SetFillStyle(3015)
    h_dw.SetLineColor(rt.kBlue)
    #h_dw.SetFillColor(rt.kBlue)
    h_nom.SetLineWidth(2)
    h_up.SetLineWidth(2)
    h_dw.SetLineWidth(2)

    canvas = rt.TCanvas("canvas","canvas", 800, 600)
    canvas.cd()
    rt.gStyle.SetOptStat(0)
    h_nom.SetTitle('')
    h_nom.GetXaxis().SetTitle("Remapped BDT")
    h_nom.GetYaxis().SetRangeUser(0.5, 1.5)

    leg = rt.TLegend(0.60, 0.70, 0.88, 0.86)
    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.032)
    leg.SetFillColor(0)
    leg.SetNColumns(1)
    leg.AddEntry(h_up, "WW Model Up", "lep")
    leg.AddEntry(h_nom, "Nominal", "lep")
    leg.AddEntry(h_dw, "WW Model Down", "lep")

    h_nom.Draw()
    h_up.Draw("same")
    h_dw.Draw("same")
    leg.Draw("same")

    canvas.SaveAs("outplots_check/ww_model_Spin2pkg1kq0_HPt300_1j.pdf")  #### change the name of the plot



