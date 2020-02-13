variables = {}
variables["ge4j_ge3t"] = [
	"Reco_Z_B1_Eta",
	"Reco_Z_B1_E",
	"Reco_Z_B1_CSV",
	"Reco_Z_B1_logPt",
	"Reco_Z_B1_logE",
	"Reco_Z_B2_Eta",
	"Reco_Z_B2_E",
	"Reco_Z_B2_CSV",
	"Reco_Z_B1_Pt",
	"Reco_Z_B2_Pt",
	"Reco_Z_B2_logPt",
	"Reco_Z_B2_logE",
	"Reco_Z_Pt",
	"Reco_Z_Eta",
	"Reco_Z_M",
	"Reco_Z_logM",
	"Reco_Z_E",
	"Reco_Z_logE",
	"Reco_Z_logPt",
	"Reco_Z_Delta_R",
	"Reco_Z_Delta_Phi",
	"Reco_Z_Delta_Eta",
	"Reco_Z_Delta_R3D",
	"Reco_Z_Boosted1_Pt",
	"Reco_Z_Boosted1_Eta",
	"Reco_Z_Boosted1_logPt",
	"Reco_Z_Boosted2_Pt",
	"Reco_Z_Boosted2_Eta",
	"Reco_Z_Boosted2_logPt",
	"Reco_Z_Angle"
	]


all_variables = list(set( [v for key in variables for v in variables[key] ] ))
