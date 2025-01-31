# Vi simulerer en portefølje med PD-estimater, en beskrivende variabel og mislighold_kommende_aar
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, FuncFormatter

N = 10000

# Custom formatter to use commas as decimal points
def comma_formatter(x, pos):
    return f'{x:.1%}'.replace('.', ',')

###########################
# PD:
# Vi bygger en dataframe med
# - PD værdier
# - En beskrivende variabel
# - Et misligholdsflag
#
# Porteføljen plottes og plot + data skrives til disk.

# N kunder med PD værdier
scale = 0.02
p_def = np.random.exponential(scale, N)
print("Gennemsnitlig PD:", p_def.mean())


# Udvælger defaults
default = np.array([np.random.choice([0, 1], p=[1 - p, p]) for p in p_def])

print("ODR:", default.sum()/N)

# Så skal vi lige have konstrueret en "variabel"
# Vi starter med at inddele p_def i 20 bins
bin_edges = np.linspace(p_def.min(), p_def.max(), 21)
bin_numbers = np.digitize(p_def, bin_edges) - 1  # Subtract 1 to make bins 0-indexed

# Så rykker vi hvert bin en op eller ned med sandsynlighed p_ryk
p_ryk = 0.05
for i in range(len(bin_numbers)):
    if np.random.rand() < p_ryk:
        bin_numbers[i] = max(0,np.random.choice([bin_numbers[i] - 1, bin_numbers[i] + 1]))

# Samler en dataframe
df_pd = pd.DataFrame({'variabel': bin_numbers, 'p_def': p_def, 'default': default})


# Plot histograms
plt.figure(figsize=(6, 4))

# Histogram of p_def
plt.hist(p_def, bins=50, alpha=0.5, label='Portefølje', edgecolor='black', density=True)
# Histogram of p_def given default = 1
plt.hist(df_pd[df_pd['default'] == 1]['p_def'], bins=50, alpha=0.5, label='Mislighold', edgecolor='black', density=True)
plt.text(0.5, 0.5, 'ODR: '+str(100*default.sum()/N)+'%', fontsize=12, transform=plt.gca().transAxes)
plt.title('Normerede PD fordelinger')
plt.xlabel('PD')
plt.ylabel('')
plt.legend()
# Format x-axis as percent with commas as decimal points
plt.gca().xaxis.set_major_formatter(FuncFormatter(comma_formatter))
plt.tight_layout()
plt.savefig('./graphics/PD_portefoelje.png')

df_pd.to_csv('./data/PD_portefoelje.csv', index=False)

###########################
# LGD:
# Vi bygger en dataframe med
# + Realiseret LGD
# + CR
# + LGL
# + LGC
# - Beregnet LGD (LGD = (1-CR)*LGL + CR*LGC)
# + Cure / Loss (Gemt som 1 for Cure, 0 for Loss)
# + Beskrivende variabel for CR
# - Beskrivende variabel for LGL
# (Ingen beskrivende variabel for LGC, da den er konstant inspireret af Privat LGD)

CureRate = 0.3  # 30% er vel ikke urimeligt
LossGivenLoss = 0.45
LossGivenCure = 0.125

# Vi starter med CR og C/L:
CR = np.random.beta(2, 5, N)  # Beta(2, 5) er en rimelig fordeling for CR
cure = np.array([np.random.choice([0, 1], p=[1 - cr, cr]) for cr in CR])

# Beskrivende variabel for CR
bin_edges = np.linspace(CR.min(), CR.max(), 21)
cr_var = np.digitize(CR, bin_edges)  # Subtract 1 to make bins 0-indexed

# Så rykker vi hvert bin en op eller ned med sandsynlighed p_ryk
p_ryk = 0.1
for i in range(len(cr_var)):
    if np.random.rand() < p_ryk:
        cr_var[i] = max(0,np.random.choice([cr_var[i] - 1, cr_var[i] + 1]))

# Så er det LGC
LGC = N*[LossGivenCure]

# LGL
mean_lgl = 0.25
spread_lgl = 0.5
LGL = np.maximum(np.random.normal(mean_lgl,spread_lgl,N),0)

# LGD
LGD = (1-CR)*LGL + CR*LGC

LGD_REAL = np.array([LGD[i] if cure[i] == 0 else LossGivenCure for i in range(N)])
# Smid noget støj på (Normalfordelt med std 0.15)
LGD_REAL_smeared = LGD_REAL +  np.random.normal(0, 0.15, N)

# Sæt til ikke at være negativ
LGD_REAL_smeared = np.maximum(LGD_REAL_smeared, 0)

df_lgl = pd.DataFrame({'CR': CR, 'LGL': LGL, 'LGC': LGC, 'LGD': LGD, 'cure': cure, 'cr_var': cr_var,'LGD_REAL': LGD_REAL})

# Plot histograms
plt.figure(figsize=(6, 4))

# Histogram af LGD
plt.hist(LGD, bins=50, alpha=0.5, label='Beregnet LGD fordeling', edgecolor='black', density=True)
plt.hist(LGD_REAL_smeared, bins=50, alpha=0.5, label='Realiseret LGD fordeling', edgecolor='black', density=True)
plt.legend()
plt.title('LGD fordelinger')
plt.xlabel('LGD')
plt.ylabel('')
plt.gca().xaxis.set_major_formatter(FuncFormatter(comma_formatter))
plt.tight_layout()
plt.savefig('./graphics/LGD_fordelinger.png')

plt.figure(figsize=(6, 4))

# Histogram af CR
plt.hist(CR, bins=50, alpha=0.5, label='CR', edgecolor='black', density=True)
plt.title('CR fordeling')
plt.xlabel('CR')
plt.ylabel('')
plt.gca().xaxis.set_major_formatter(FuncFormatter(comma_formatter))
plt.text(0.5, 0.5, 'Obs. Cure Rate: '+str(100*cure.sum()/N)+'%', fontsize=12, transform=plt.gca().transAxes)
plt.tight_layout()
plt.savefig('./graphics/CR_fordeling.png')

# Histogram af LGL
plt.figure(figsize=(6, 4))
plt.hist(LGL, bins=50, alpha=0.5, label='LGL', edgecolor='black', density=True)
plt.title('LGL fordeling')
plt.xlabel('LGL')
plt.ylabel('')
plt.gca().xaxis.set_major_formatter(FuncFormatter(comma_formatter))
plt.text(0.5, 0.5, 'Obs. LGL: {:.2%}'.format((LGL*(1-CR)).mean()), fontsize=12, transform=plt.gca().transAxes)
plt.tight_layout()
plt.savefig('./graphics/LGL_fordeling.png')

# Gem dataframe
df_lgl.to_csv('./data/LGD_portefoelje.csv', index=False)

pass