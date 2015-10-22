import ROOT as rt
import os

py6 = rt.TFile.Open("py6_25bin/py6_me_25bins.root")
her = rt.TFile.Open("her_me.root")

py6_bdt0=py6.Get("MVAOutput0_20bins_0jet_emu_all")
py6_bdt2=py6.Get("MVAOutput2_20bins_0jet_emu_all")

#her_bdt0=her.Get("MVAOutput0_20bins_0jet_emu_all")
#her_bdt2=her.Get("MVAOutput2_20bins_0jet_emu_all")
#

py6_bdt0.Scale(1/py6_bdt0.Integral())
py6_bdt2.Scale(1/py6_bdt2.Integral())

#her_bdt0.Scale(1/her_bdt0.Integral())
#her_bdt2.Scale(1/her_bdt2.Integral())
#
#ratio_bdt0 = her_bdt0.Clone()
#ratio_bdt2 = her_bdt2.Clone()
#
#ratio_bdt0.Divide(py6_bdt0)
#ratio_bdt2.Divide(py6_bdt2)

canvas1 = rt.TCanvas("bdt0","bdt0", 800,600)

#her_bdt0.SetLineColor(rt.kRed)
#her_bdt2.SetLineColor(rt.kRed)
#
#py6_bdt0.SetLineColor(rt.kBlue)
#py6_bdt2.SetLineColor(rt.kBlue)
#

canvas1.cd()
#her_bdt0.SetTitle("Red=Herwig")
#her_bdt0.Draw()
py6_bdt0.Draw()


canvas2 = rt.TCanvas("bdt2","bdt2", 800,600)
canvas2.cd()
#her_bdt2.SetTitle("Red=Herwig")
#her_bdt2.Draw()
py6_bdt2.Draw()

canvas1.SaveAs("py6_25bins_bdt0.pdf")
canvas2.SaveAs("py6_25bins_bdt2.pdf")



##### RATIOS
#canvas3 = rt.TCanvas("ratio_bdt0","ratio_bdt0", 800,600)
#canvas3.cd()
#ratio_bdt0.Draw()
#
#canvas4 = rt.TCanvas("ratio_bdt2","ratio_bdt2", 800,600)
#canvas4.cd()
#ratio_bdt2.Draw()
#
#rat0, rat2 = [],[]
## values for ratios:
#for ibin in range(1, 21):
#    rat0_val = ratio_bdt0.GetBinContent(ibin)
#    rat2_val = ratio_bdt2.GetBinContent(ibin)
#    rat0.append(rat0_val)
#    rat2.append(rat2_val)
#
#
#
#print rat0 , ' -- '
#print rat2 , '---'
#canvas3.SaveAs("ratio_bdt0.pdf")
#canvas4.SaveAs("ratio_bdt2.pdf")
