variables = {}

variables["ge4j_ge4t"] = [
    "Reco_JABDT_ttbar_Jet_CSV_whaddau2",
    "Evt_Deta_JetsAverage",
    "Reco_JABDT_ttbar_Jet_CSV_whaddau1",
    "Evt_CSV_avg_tagged",
    "Reco_JABDT_tHW_Jet_CSV_whaddau1",
    "Reco_JABDT_tHq_abs_ljet_eta",
    "Reco_JABDT_ttbar_Jet_CSV_btoplep",
    "Evt_M_JetsAverage",
    "CSV[1]",
    "Evt_Pt_JetsAverage",
    "Reco_tHW_top_h_dr",
    "Evt_M_minDrLepTag",
    "TaggedJet_M[0]",
    "Reco_JABDT_ttH_Jet_CSV_hdau2",
    "Reco_ttH_toplep_m",
    "Reco_JABDT_ttH_Jet_CSV_btoplep",
    "Evt_M2_TaggedJetsAverage",
    "Evt_CSV_avg",
    "Reco_JABDT_tHW_top_pt__P__h_pt__P__wb_pt__DIV__Evt_HT__P__Evt_Pt_MET__P__Lep_Pt",
    "Reco_ttH_bestJABDToutput",
    "Reco_ttbar_toplep_m",
    "Reco_tHq_bestJABDToutput",
    "Reco_JABDT_tHW_Jet_CSV_btop",
    "Reco_tHW_whaddau_m1",
    "Reco_JABDT_tHW_Jet_CSV_hdau2",
    "Reco_JABDT_ttH_log_toplep_m",
    "Reco_tHW_bestJABDToutput",
    "Reco_JABDT_tHq_ljet_e__M__btop_e",
    "Reco_ttbar_bestJABDToutput",
    "N_BTagsM",
    "Evt_M_TaggedJetsAverage",
    "Reco_tHW_whad_dr",
    "N_Jets",
    "CSV[2]",
    "Reco_JABDT_tHq_Jet_CSV_hdau1",
    "Evt_Deta_TaggedJetsAverage",
    "Reco_JABDT_tHq_Jet_CSV_btop",
    "Evt_Pt_minDrTaggedJets",
    "Reco_tHq_costhetastar",
    "Evt_M2_JetsAverage",
    "Evt_Dr_minDrTaggedJets",
    "Evt_blr_transformed",
    ]


variables["ge4j_3t"] = [
    "Reco_JABDT_ttbar_Jet_CSV_whaddau2",
    "Evt_Deta_JetsAverage",
    "Reco_JABDT_ttbar_Jet_CSV_whaddau1",
    "Evt_CSV_avg_tagged",
    "Reco_JABDT_tHW_Jet_CSV_whaddau1",
    "Reco_JABDT_ttH_Jet_CSV_hdau2",
    "Reco_JABDT_ttbar_Jet_CSV_btophad",
    "Reco_JABDT_ttbar_Jet_CSV_btoplep",
    "Evt_M_JetsAverage",
    "Evt_CSV_min_tagged",
    "Evt_HT_tags",
    "Reco_JABDT_tHq_log_ljet_pt",
    "Reco_ttbar_whad_m",
    "Reco_JABDT_tHW_log_top_m",
    "Reco_JABDT_ttH_Jet_CSV_btoplep",
    "Evt_CSV_avg",
    "Evt_M_Total",
    "Reco_ttH_bestJABDToutput",
    "Reco_ttbar_toplep_m",
    "Evt_M2_JetsAverage",
    "Reco_tHq_bestJABDToutput",
    "CSV[1]",
    "Evt_Pt_JetsAverage",
    "Evt_CSV_dev",
    "Reco_tHW_bestJABDToutput",
    "Reco_JABDT_tHW_Jet_CSV_btop",
    "Evt_Dr_JetsAverage",
    "Evt_M_TaggedJetsAverage",
    "Reco_ttbar_bestJABDToutput",
    "N_Jets",
    "Evt_JetPt_over_JetE",
    "Evt_Deta_TaggedJetsAverage",
    "Reco_JABDT_ttbar_log_tophad_m",
    "Reco_tHW_whad_dr",
    "Evt_Pt_minDrTaggedJets",
    "Reco_tHq_ljet_m",
    "Reco_JABDT_tHW_log_wb_m",
    "Reco_JABDT_ttbar_log_whad_m",
    "Evt_h1",
    "Evt_blr_transformed",
    ]

all_variables = list(set( [v for key in variables for v in variables[key] ] ))