# preperations
import numpy as np
import matplotlib.pyplot as plt

############################################################################
# Set File Paths
# Please set the path for pp jet data file
file_pp = '../../data/jet_pp.dat'

# Please set the path for pbpb jet data file
file_pbpb = '../../data/jet_pbpb.dat'

# Please set the value of jet cone size you used in the jet reconstruction
jetR = 0.4

# Number of hard scattering events generated by JETSCAPE
n_ev_pp = 250
n_ev_pbpb = 250

############################################################################
# preperations
import numpy as np
import matplotlib.pyplot as plt

# pi and 2pi coppied from FastJet
twopi = 6.283185307179586476925286766559005768394
pi = 0.5*twopi

# define plot style
width = 0.05
plotMarkerSize = 8
labelfontsize = 15
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = [6., 4.5]
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['xtick.top'] = True
mpl.rcParams['xtick.labelsize'] = 15
mpl.rcParams['xtick.major.width'] = 1.0
mpl.rcParams['xtick.minor.width'] = 0.8
mpl.rcParams['xtick.minor.visible'] = True
mpl.rcParams['xtick.direction'] = "in"
mpl.rcParams['ytick.right'] = True
mpl.rcParams['ytick.labelsize'] = 15
mpl.rcParams['ytick.major.width'] = 1.0
mpl.rcParams['ytick.minor.width'] = 0.8
mpl.rcParams['ytick.minor.visible'] = True
mpl.rcParams['ytick.direction'] = "in"
mpl.rcParams['legend.fontsize'] = 15
mpl.rcParams['legend.numpoints'] = 1
mpl.rcParams['font.size'] = 15
mpl.rcParams['savefig.format'] = "pdf"
############################################################################
def ratio_error(v1,e1,v2,e2):
  #v1, e1: numerator value and error
  #v2, e2: denominator value and error  
  error1 = e1/v2
  error2 = (e2/v2)*(v1/v2)
  error = np.sqrt(error1*error1+error2*error2)
  return error
############################################################################
# Load files
data_pp = np.loadtxt(file_pp, delimiter=',')
data_pbpb = np.loadtxt(file_pbpb, delimiter=',')

# Indices of the data array
i_pp = data_pp[:,0] 
i_pbpb = data_pbpb[:,0] 

# Get Indices of jets in the data array
jet_id_pp = np.where(i_pp < 0.1)
jet_id_pbpb = np.where(i_pbpb < 0.1)

# Extract jets
jets_pp = data_pp[jet_id_pp]
jets_pbpb = data_pbpb[jet_id_pbpb]

# Extract associated charged particles for pp
assoc_pp= []
for i in range(len(jet_id_pp[0])-1):
  chunck = data_pp[jet_id_pp[0][i]+1:jet_id_pp[0][i+1]]
  assoc_pp.append(chunck)
chunck = data_pp[jet_id_pp[0][-1]+1:]
assoc_pp.append(chunck)

# Extract associated charged particles for pbpb
assoc_pbpb= []
for i in range(len(jet_id_pbpb[0])-1):
  chunck = data_pbpb[jet_id_pbpb[0][i]+1:jet_id_pbpb[0][i+1]]
  assoc_pbpb.append(chunck)
chunck = data_pbpb[jet_id_pbpb[0][-1]+1:]
assoc_pbpb.append(chunck)
############################################################################
## Jet Spectrum
############################################################################
# Prepare arrays of Jet-pT
jet_pt_pp_in = jets_pp[:,1]
jet_pt_pbpb_in = jets_pbpb[:,1]

# bin settings
pt_min = 110
pt_max = 150
pt_bins = np.linspace(pt_min, pt_max,4)

# Fill Histogram
n_pp, pt = np.histogram(jet_pt_pp_in, bins=pt_bins )
n_pbpb, pt = np.histogram(jet_pt_pbpb_in, bins=pt_bins )

# Statistical Errors
err_n_pp = np.sqrt(n_pp)
err_n_pbpb = np.sqrt(n_pbpb)

# bin width
dpt = (pt[1:]-pt[:-1])
# bin center
pt = pt[0:-1] + 0.5*dpt

# Jet Spectrum 
dn_dpt_pp = n_pp/n_ev_pp/dpt
dn_dpt_pbpb = n_pbpb/n_ev_pbpb/dpt

# Errors 
err_dn_dpt_pp = err_n_pp/n_ev_pp/dpt
err_dn_dpt_pbpb = err_n_pbpb/n_ev_pbpb/dpt

# Generate Plots
fig = plt.figure()

plt.errorbar(pt, dn_dpt_pp, fmt='s', label="pp",
             xerr=0.5*dpt, yerr=err_dn_dpt_pp, color='black')

plt.errorbar(pt, dn_dpt_pbpb, fmt='o', label="PbPb(30-40%)",
             xerr=0.5*dpt, yerr=err_dn_dpt_pbpb, color='red')

#axes setting
plt.yscale('log')
plt.legend(loc=0)
plt.xlabel(r"$p^{\mathrm{jet}}_{\mathrm{T}}$ [GeV]")
plt.ylabel(r"$(1/N_{\mathrm{ev}})dN_{\mathrm{jet}}/dp^{\mathrm{jet}}_{\mathrm{T}}$")
plt.xlim(pt_min,pt_max)
y_min = dn_dpt_pbpb[-1]*0.5
if y_min < 0:
  y_min = 0.0015

y_max = (dn_dpt_pp[0]+err_dn_dpt_pp[0])*2.0
plt.ylim(y_min,y_max)
plt.text(pt_min+1,y_min*1.2, '5.02 TeV')

# save plots
plt.tight_layout()

print('Find n_jet.pdf')
plt.savefig('n_jet')
############################################################################
## Jet RAA
############################################################################
# Generate Plots
fig = plt.figure()

# Calculate RAA and error
raa =  dn_dpt_pbpb/dn_dpt_pp
error_raa = ratio_error(dn_dpt_pbpb,err_dn_dpt_pbpb,dn_dpt_pp,err_dn_dpt_pp)

plt.errorbar(pt, raa, fmt='o', label="PbPb(30-40%)/pp",
             xerr=0.5*dpt, yerr=error_raa, color='red')


#axes setting
plt.legend(loc=0)
plt.xlabel(r"$p^{\mathrm{jet}}_{\mathrm{T}}$ [GeV]")
plt.ylabel(r"$R^{\mathrm{jet}}_{\mathrm{AA}}$")
plt.xlim(pt_min,pt_max)
plt.ylim(0.0,1.2)
plt.legend(loc=0)
plt.text(pt_min+1,1.07, '5.02 TeV')
plt.axhline(1, color = "black", linestyle="dashed", linewidth=0.8) 

# save plot to the Desktop
plt.tight_layout()
print('Find raa.pdf')
plt.savefig('raa')
############################################################################