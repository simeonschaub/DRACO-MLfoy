variables = {}

variables["ge4j_3t"] = [
    "Evt_Deta_JetsAverage",
    "Evt_HT_tags",
    "Evt_MTW",
    "Evt_CSV_avg_tagged",
    "CSV[2]",
    "Jet_Pt[0]",
    "Evt_CSV_min_tagged",
    "Evt_Dr_minDrTaggedJets",
    "Evt_Pt_TaggedJetsAverage",
    "Evt_CSV_dev_tagged",
    "Jet_DeepJetCSV[0]",
    "Evt_M_JetsAverage",
    "Evt_Deta_TaggedJetsAverage",
    "Evt_M2_TaggedJetsAverage",
    "Evt_M_minDrLepTag",
    "Evt_M2_minDrTaggedJets",
    "Evt_CSV_avg",
    "Evt_Pt_minDrTaggedJets",
    "Evt_M_Total",
    "Evt_M_TaggedJetsAverage",
    "data_era",
    ]

all_variables = list(set( [v for key in variables for v in variables[key] ] ))
