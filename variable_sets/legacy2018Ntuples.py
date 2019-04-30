variables = {}
variables["4j_ge3t"] = [
    'Evt_CSV_Average_Tagged',
    'Evt_CSV_Min',
    'Evt_CSV_Min_Tagged',
    'Evt_Dr_JetsAverage',
    'Evt_Dr_MinDeltaRJets',
    'Evt_Dr_MinDeltaRLeptonJet',
    'Evt_Dr_MinDeltaRLeptonTaggedJet',
    'Evt_Dr_MinDeltaRTaggedJets',
    'Evt_Dr_TaggedJetsAverage',
    'Evt_Eta_JetsAverage',
    'Evt_Eta_TaggedJetsAverage',
    'Evt_HT_Jets',
    'Evt_JetPtOverJetE',
    'Evt_Jet_MaxDeta_Jets',
    'Evt_M2_JetsAverage',
    'Evt_M_JetsAverage',
    'Evt_M_MedianTaggedJets',
    'Evt_M_MinDeltaRJets',
    'Evt_M_MinDeltaRLeptonJet',
    'Evt_M_MinDeltaRLeptonTaggedJet',
    'Evt_M_MinDeltaRTaggedJets',
    'Evt_M_TaggedJetsAverage',
    'Evt_Pt_MET',
    'Evt_Pt_MinDeltaRJets',
    'Evt_Pt_MinDeltaRTaggedJets',
    'MVA_Evt_CSV_Average',
    'MVA_Evt_Deta_JetsAverage',
    'MVA_Evt_Deta_TaggedJetsAverage',
    'MVA_Evt_M2_TaggedJetsAverage',
    'MVA_HT',
    'MVA_HT_tag',
    'MVA_M3',
    'MVA_MET',
    'MVA_MHT',
    'MVA_Mlb',
    'MVA_all_sum_pt_with_met',
    'MVA_aplanarity',
    'MVA_aplanarity_jets',
    'MVA_aplanarity_tags',
    'MVA_avg_btag_disc_btags',
    'MVA_avg_dr_tagged_jets',
    'MVA_blr',
    'MVA_blr_transformed',
    'MVA_closest_tagged_dijet_mass',
    'MVA_cos_theta_blep_bhad',
    'MVA_cos_theta_l_bhad',
    'MVA_delta_eta_blep_bhad',
    'MVA_delta_eta_l_bhad',
    'MVA_delta_phi_blep_bhad',
    'MVA_delta_phi_l_bhad',
    'MVA_dev_from_avg_disc_btags',
    'MVA_dr_between_lep_and_closest_jet',
    'MVA_h0',
    'MVA_h1',
    'MVA_h2',
    'MVA_h3',
    'MVA_invariant_mass_of_everything',
    'MVA_lowest_btag',
    'MVA_max_dR_bb',
    'MVA_max_dR_jj',
    'MVA_maxeta_jet_jet',
    'MVA_maxeta_jet_tag',
    'MVA_maxeta_tag_tag',
    'MVA_pt_all_jets_over_E_all_jets',
    'MVA_pt_all_jets_over_E_all_jets_tags',
    'MVA_sphericity',
    'MVA_sphericity_jets',
    'MVA_sphericity_tags',
    'MVA_tagged_dijet_mass_closest_to_125',
    'MVA_transverse_sphericity',
    'MVA_transverse_sphericity_jets',
    'MVA_transverse_sphericity_tags',
    'N_BTagsL',
    'N_BTagsM',
    'N_BTagsT',
    'N_LooseJets',
    'N_PrimaryVertices',
    'CSV[0]',
    'CSV[1]',
    'CSV[2]',
    'CSV[3]',
    'Jet_DeepJetCSV[0]',
    'Jet_DeepJetCSV[1]',
    'Jet_DeepJetCSV[2]',
    'Jet_DeepJetCSV[3]',
    'Jet_DeepJet_b[0]',
    'Jet_DeepJet_b[1]',
    'Jet_DeepJet_b[2]',
    'Jet_DeepJet_b[3]',
    'Jet_DeepJet_bb[0]',
    'Jet_DeepJet_bb[1]',
    'Jet_DeepJet_bb[2]',
    'Jet_DeepJet_bb[3]',
    'Jet_DeepJet_c[0]',
    'Jet_DeepJet_c[1]',
    'Jet_DeepJet_c[2]',
    'Jet_DeepJet_c[3]',
    'Jet_DeepJet_g[0]',
    'Jet_DeepJet_g[1]',
    'Jet_DeepJet_g[2]',
    'Jet_DeepJet_g[3]',
    'Jet_DeepJet_lepb[0]',
    'Jet_DeepJet_lepb[1]',
    'Jet_DeepJet_lepb[2]',
    'Jet_DeepJet_lepb[3]',
    'Jet_DeepJet_uds[0]',
    'Jet_DeepJet_uds[1]',
    'Jet_DeepJet_uds[2]',
    'Jet_DeepJet_uds[3]',
    'Jet_E[0]',
    'Jet_E[1]',
    'Jet_E[2]',
    'Jet_E[3]',
    'Jet_Eta[0]',
    'Jet_Eta[1]',
    'Jet_Eta[2]',
    'Jet_Eta[3]',
    'Jet_M[0]',
    'Jet_M[1]',
    'Jet_M[2]',
    'Jet_M[3]',
    'Jet_Phi[0]',
    'Jet_Phi[1]',
    'Jet_Phi[2]',
    'Jet_Phi[3]',
    'Jet_Pt[0]',
    'Jet_Pt[1]',
    'Jet_Pt[2]',
    'Jet_Pt[3]',
    'LooseLepton_E[0]',
    'LooseLepton_Eta[0]',
    'LooseLepton_Phi[0]',
    'LooseLepton_Pt[0]',
    ]
variables["ge4j_ge3t"] = variables["4j_ge3t"]
variables["le5j_ge3t"] = variables["4j_ge3t"]

variables["5j_ge3t"] = variables["4j_ge3t"] + [
    'CSV[4]',
    'Jet_DeepJetCSV[4]',
    'Jet_DeepJet_b[4]',
    'Jet_DeepJet_bb[4]',
    'Jet_DeepJet_c[4]',
    'Jet_DeepJet_g[4]',
    'Jet_DeepJet_lepb[4]',
    'Jet_DeepJet_uds[4]',
    'Jet_E[4]',
    'Jet_Eta[4]',
    'Jet_M[4]',
    'Jet_Phi[4]',
    'Jet_Pt[4]',
    ]

variables["ge6j_ge3t"] = variables["5j_ge3t"] + [
    'MVA_dEta_fn',
    'MVA_best_higgs_mass',
    'CSV[5]',
    'Jet_DeepJetCSV[5]',
    'Jet_DeepJet_b[5]',
    'Jet_DeepJet_bb[5]',
    'Jet_DeepJet_c[5]',
    'Jet_DeepJet_g[5]',
    'Jet_DeepJet_lepb[5]',
    'Jet_DeepJet_uds[5]',
    'Jet_E[5]',
    'Jet_Eta[5]',
    'Jet_M[5]',
    'Jet_Phi[5]',
    'Jet_Pt[5]',
    ]


all_variables = list(set( [v for key in variables for v in variables[key] ] ))
