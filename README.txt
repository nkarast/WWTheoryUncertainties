=== 
===	WW Theory Uncertainties
===
=== 	@ Nikos Karastathis < nkarast .at. cern .dot. ch >
===

=== README

This is to calculate the theory uncertainties on the WW shape for the unrolled BDT distribution of the H->WW->lvlv Spin/CP analysis

Step 1. Run the BuildBDTs/runall_applybdt.py on the theory ntuples to get the truth level BDT distribution per channel (i.e. per training)

Step 2: Run the MakeSelections/makeSelection_0j.py (or 1j.py) to apply the event selection used in the analysis, and create the final hist files

Step 3: Run the Envelopes/unroll_model.py or Envelopes/unroll_ueps.py to get the .dat files with the per bin variations on the unrolled BDT distribution

Optional:
There are some plotting macros under draw_macros/ to plot the envelope around the nominal WW 

