
#ROOT.gROOT.ProcessLine('.L $HOME/public/spin-ueps/bdt/mtt.c+')

ROOT.gROOT.ProcessLine('.L /glusterfs/atlas2/users/nikosk/spin-ueps/bdt/mtt.c+')

rmap = { 'transmass/0.001' : 'MT_TrackHWW_Clj',
         'mll/0.001' : 'Mll',
         'ptll/0.001' : 'Ptll',
         'phill' : 'DPhill',
         'met/0.001' : 'MET_TrackHWW_Clj',
         'max(-1,util::mtt(mll, lep1_pt, lep1_phi, lep2_pt, lep2_phi, met, met_phi)/0.001)' : 'max(-1,Mtt_TrackHWW_Clj)',
         'abs(lep1_pt-lep2_pt)/0.001' : 'abs(DPt)',
         'lep1_pt>lep2_pt?(lep1_pt-0.5*lep2_pt+0.5*met):(lep2_pt-0.5*lep1_pt+0.5*met)' : \
              'lepPt0>lepPt1?(lepPt0-0.5*lepPt1+0.5*MET_TrackHWW_Clj):(lepPt1-0.5*lepPt0+0.5*MET_TrackHWW_Clj)' }


aliases = {}
for k,v in rmap.items():
    aliases[v] = k
