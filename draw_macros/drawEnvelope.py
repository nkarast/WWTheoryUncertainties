import ROOT as rt
import glob

debug = 1

def setstyle():
    rt.gStyle.SetOptStat(0);
    rt.gStyle.SetFillColor(10);
    rt.gStyle.SetFrameFillColor(10);
    rt.gStyle.SetCanvasColor(10);
    rt.gStyle.SetPadColor(10);
    rt.gStyle.SetTitleFillColor(0);
    rt.gStyle.SetStatColor(10);

    rt.gStyle.SetCanvasBorderMode(0);
    rt.gStyle.SetFrameBorderMode(0);
    rt.gStyle.SetPadBorderMode(0);
    rt.gStyle.SetDrawBorder(0);
    rt.gStyle.SetTitleBorderSize(0);

    rt.gStyle.SetFuncWidth(2);
    rt.gStyle.SetHistLineWidth(2);
    rt.gStyle.SetFuncColor(2);

    rt.gStyle.SetPadTopMargin(0.05)
    rt.gStyle.SetPadBottomMargin(0.16);
    rt.gStyle.SetPadLeftMargin(0.16);
    rt.gStyle.SetPadRightMargin(0.05);

    rt.gStyle.SetPadTickX(1);
    rt.gStyle.SetPadTickY(1);
    rt.gStyle.SetFrameLineWidth(1);
    rt.gStyle.SetLineWidth(1);


def HSG3HistStyle(histo):
    histo.SetTitle("");
    histo.SetLineWidth(3);
    histo.SetTitleSize(0.07,"x");
    histo.SetTitleSize(0.07,"y");
    histo.SetNdivisions(505,"x");
    histo.SetNdivisions(505,"y");
    histo.SetLabelSize(0.07,"x");
    histo.SetLabelSize(0.07,"y");
    histo.SetTitleOffset(1.,"x");
    histo.SetTitleOffset(1.,"y");

for filename in glob.glob("/Users/nkarast/Documents/Higgs/Work/CPMixing/TheoryNtuples/finalVersionOfCode/UEPS/*.dat"):

    setstyle()
    file = open(filename, 'read')
    print 'Working with ', filename
    # bin_contents = bincontents[]
    # nbins = len(bincontents)
    bincontents = []
    nominalContent = []
    for line in file.readlines():
        if "#" in line : continue
        bincontents.append(float(line.split()[0]))
        nominalContent.append(1.)

    file.close()

    hist_nom = rt.TH1F("Nominal","Nominal", len(bincontents), 0, len(bincontents))
    hist_one = rt.TH1F("Ones","Ones", len(bincontents), 0, len(bincontents))

    for bin in range(len(bincontents)):
        hist_nom.SetBinContent(bin+1, 1.)
        hist_one.SetBinContent(bin+1, 1.)
        if bincontents[bin]==1 :
            bincontents[bin]=0.
        
        hist_nom.SetBinError(bin+1, bincontents[bin])


    canvas = rt.TCanvas("WW","WW", 800, 600)
    canvas.cd()
    HSG3HistStyle(hist_nom)
    HSG3HistStyle(hist_nom)
    hist_nom.SetTitle("")
    rt.gStyle.SetOptStat(0)
    hist_nom.SetMinimum(0)
    hist_nom.GetXaxis().SetTitle("BDT Output")
    hist_nom.GetYaxis().SetTitle("Variation")
    hist_nom.SetMaximum(2.5)
    hist_nom.SetFillColor(46)
    hist_nom.SetFillStyle(3001)
    hist_nom.SetLineColor(46)
    hist_nom.Draw("E2")

    hist_one.SetLineColor(rt.kBlack)
    hist_one.SetLineWidth(2)
    hist_one.Draw("same")

    leg = rt.TLegend(0.60, 0.70, 0.90, 0.90)
    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.045)
    leg.SetFillColor(0)
    leg.SetNColumns(1)
    leg.AddEntry(hist_one, "Nominal", "l")
    leg.AddEntry(hist_nom, "WW UE/PS", "f")
    leg.Draw("same")

    lumi = rt.TLatex();
    lumi.SetNDC();
    lumi.SetTextFont(42);
    lumi.SetTextSize(0.045);
    lumi.SetTextColor(1);
    lumi.DrawLatex(0.22, 0.8, "Simulation   #sqrt{s} = 8 TeV")
    lumi.DrawLatex(0.2, 0.70, "#sqrt{s} = 8 TeV,  #int L dt = 20.3 fb^{-1}")

    savename = filename[:-4]+"_wwUEPS.pdf"
    canvas.SaveAs(savename)

    print bincontents