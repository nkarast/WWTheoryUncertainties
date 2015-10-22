import ROOT as rt

file_amc_0j = rt.TFile.Open("../histfiles/final_amcatnlo_0jet.root")
file_amc_1j = rt.TFile.Open("../histfiles/final_amcatnlo_1jet.root")

file_her_0j = rt.TFile.Open("../histfiles/final_herwig_0jet.root")
file_her_1j = rt.TFile.Open("../histfiles/final_herwig_1jet.root")

amc_0j = file_amc_0j.Get("bdt_spin2pkg05kq1_hpt125_0jet")
amc_1j = file_amc_1j.Get("bdt_spin2pkg05kq1_hpt125_1jet")

her_0j = file_her_0j.Get("bdt_spin2pkg05kq1_hpt125_0jet")
her_1j = file_her_1j.Get("bdt_spin2pkg05kq1_hpt125_1jet")

amc_0j.Scale(1/amc_0j.Integral())
amc_1j.Scale(1/amc_1j.Integral())

her_0j.Scale(1/her_0j.Integral())
her_1j.Scale(1/her_1j.Integral())


amc_0j.SetLineWidth(2)
amc_1j.SetLineWidth(2)
her_0j.SetLineWidth(2)
her_1j.SetLineWidth(2)

amc_1j.SetLineColor(rt.kRed)
amc_0j.SetLineColor(rt.kRed)

rt.gStyle.SetOptStat(0)

#canvas_1 = rt.TCanvas("amc_spin2pkg05_hpt125","amc_spin2pkg05_hpt125",800,600)
#canvas_1.cd()
#amc_0j.SetTitle("amc@nlo 0 & 1(red)j")
#amc_0j.Draw()
#amc_1j.Draw("same")
#
#
#canvas_2 = rt.TCanvas("her_spin2pkg05_hpt125","her_spin2pkg05_hpt125",800,600)
#canvas_2.cd()
#her_0j.SetTitle("powheg 0 & 1(red)j")
#her_0j.Draw()
#her_1j.Draw("same")
#
#canvas_1.SaveAs("amc_01jet_bdt2.pdf")
#canvas_2.SaveAs("her_01jet_bdt2.pdf")

canvas_3 = rt.TCanvas("amcher_0j","amcher_0j",800,600)
canvas_3.cd()
amc_0j.SetTitle("BDT2 0j (amc=red)")
amc_0j.Draw("h")
her_0j.Draw("hsame")



canvas_4 = rt.TCanvas("amcher_1j","amcher_1j",800,600)
canvas_4.cd()
amc_1j.SetTitle("BDT2 1j (amc=red)")
amc_1j.Draw("h")
her_1j.Draw("hsame")

canvas_3.SaveAs("bdt2_0j_amcpowheg.pdf")
canvas_4.SaveAs("bdt2_1j_amcpowheg.pdf")

print 'amc@nlo\t\t|\tpowheg - 0j'
for ibin in range(1, amc_0j.GetNbinsX()+1):
    print '%0.10f\t|\t%0.10f' % (amc_0j.GetBinContent(ibin) , her_0j.GetBinContent(ibin))

print '-----------------------------------------------'

print 'amc@nlo\t\t|\tpowheg - 1j'
for ibin in range(1, amc_1j.GetNbinsX()+1):
    print '%0.10f\t|\t%0.10f' % (amc_1j.GetBinContent(ibin) , her_1j.GetBinContent(ibin))
