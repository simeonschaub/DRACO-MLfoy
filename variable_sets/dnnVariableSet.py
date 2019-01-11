variables = {}
variables["4j_ge3t"] = [
    'Jet_Pt[0]',
    'Jet_CSV[0]',
    'Jet_Eta[1]',
    'Jet_CSV[1]',
    'Jet_Eta[2]',
    'Jet_CSV[2]',
    'Jet_Pt[3]',
    'Jet_Eta[3]',
    'Jet_CSV[3]',
    'LooseLepton_Eta[0]',
    'BDT_common5_input_HT_tag',
    'Evt_Dr_MinDeltaRJets',
    'Evt_Dr_MinDeltaRTaggedJets',
    'BDT_common5_input_aplanarity_tags',
    'BDT_common5_input_sphericity_jets',
    'BDT_common5_input_transverse_sphericity_jets',
    'BDT_common5_input_transverse_sphericity_tags',
    'Evt_CSV_Average',
    'Evt_CSV_Average_Tagged',
    'CSV[0]',
    'Evt_CSV_Min',
    'Evt_CSV_Min_Tagged',
    'Evt_Dr_MinDeltaRLeptonJet',
    'BDT_common5_input_h2',
    'BDT_common5_input_h3',
    'Evt_M_MinDeltaRLeptonTaggedJet',
    'BDT_common5_input_closest_tagged_dijet_mass',
    'BDT_common5_input_dev_from_avg_disc_btags',
    'Evt_M_JetsAverage',
    'Evt_M2_TaggedJetsAverage',
    'N_BTagsT',
    'CSV[1]',
    'Evt_blr_ETH',
    'Evt_blr_ETH_transformed',
    'memDBp',
    ]


variables["5j_ge3t"] = [
    'Jet_Pt[0]',
    'Jet_Eta[0]',
    'Jet_CSV[0]',
    'Jet_Pt[1]',
    'Jet_Eta[1]',
    'Jet_CSV[1]',
    'Jet_Pt[2]',
    'Jet_Eta[2]',
    'Jet_CSV[2]',
    'Jet_Pt[3]',
    'Jet_Eta[3]',
    'LooseLepton_Pt[0]',
    'Evt_HT',
    'BDT_common5_input_HT_tag',
    'Evt_Dr_MinDeltaRJets',
    'Evt_Dr_MinDeltaRTaggedJets',
    'BDT_common5_input_max_dR_jj',
    'BDT_common5_input_aplanarity_jets',
    'BDT_common5_input_aplanarity_tags',
    'BDT_common5_input_sphericity_jets',
    'BDT_common5_input_sphericity_tags',
    'BDT_common5_input_transverse_sphericity_jets',
    'BDT_common5_input_transverse_sphericity_tags',
    'Evt_CSV_Average',
    'Evt_CSV_Average_Tagged',
    'CSV[0]',
    'Evt_CSV_Min',
    'Evt_CSV_Min_Tagged',
    'Evt_Dr_MinDeltaRLeptonJet',
    'Evt_Dr_MinDeltaRLeptonTaggedJet',
    'BDT_common5_input_h1',
    'BDT_common5_input_h2',
    'Evt_M_MinDeltaRLeptonTaggedJet',
    'Evt_Dr_TaggedJetsAverage',
    'BDT_common5_input_closest_tagged_dijet_mass',
    'BDT_common5_input_dev_from_avg_disc_btags',
    'Evt_M_JetsAverage',
    'N_BTagsT',
    'BDT_common5_input_tagged_dijet_mass_closest_to_125',
    'CSV[1]',
    'Evt_blr_ETH',
    'Evt_blr_ETH_transformed',
    'memDBp',
    ]


variables["ge6j_ge3t"] = [
    'Jet_Eta[0]',
    'Jet_CSV[0]',
    'Jet_Eta[1]',
    'Jet_CSV[1]',
    'Jet_Eta[2]',
    'Jet_CSV[2]',
    'Jet_Eta[3]',
    'Jet_CSV[3]',
    'LooseLepton_Pt[0]',
    'LooseLepton_Eta[0]',
    'BDT_common5_input_HT_tag',
    'Evt_Dr_MinDeltaRJets',
    'Evt_Dr_MinDeltaRTaggedJets',
    'BDT_common5_input_max_dR_bb',
    'BDT_common5_input_aplanarity_jets',
    'BDT_common5_input_aplanarity_tags',
    'Evt_JetPtOverJetE',
    'BDT_common5_input_pt_all_jets_over_E_all_jets_tags',
    'BDT_common5_input_sphericity_jets',
    'BDT_common5_input_sphericity_tags',
    'BDT_common5_input_transverse_sphericity_jets',
    'BDT_common5_input_transverse_sphericity_tags',
    'Evt_CSV_Average',
    'Evt_CSV_Average_Tagged',
    'CSV[0]',
    'Evt_CSV_Min',
    'Evt_CSV_Min_Tagged',
    'Evt_Dr_MinDeltaRLeptonTaggedJet',
    'BDT_common5_input_h3',
    'Evt_M_MinDeltaRLeptonTaggedJet',
    'Evt_Deta_TaggedJetsAverage',
    'Evt_Dr_TaggedJetsAverage',
    'BDT_common5_input_closest_tagged_dijet_mass',
    'BDT_common5_input_dev_from_avg_disc_btags',
    'Evt_M_JetsAverage',
    'Evt_M2_TaggedJetsAverage',
    'N_BTagsT',
    'BDT_common5_input_tagged_dijet_mass_closest_to_125',
    'CSV[1]',
    'Evt_blr_ETH',
    'Evt_blr_ETH_transformed',
    'memDBp',
    ]

all_variables = set( [v for key in variables for v in variables[key] ] )
