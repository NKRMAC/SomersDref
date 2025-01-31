import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt
from scipy.stats import somersd

# Indlæser data
df_pd = pd.read_csv('data/PD_portefoelje.csv')

# True labels (defaults)
y_true = df_pd['default']

# Estimerede sandsynligheder
y_scores = df_pd['p_def']

# Beregner ROCkurve
fpr, tpr, thresholds = roc_curve(y_true, y_scores)

# AUC
auc = roc_auc_score(y_true, y_scores)

# Plotter ROCkurve
plt.figure(figsize=(6, 4))
plt.plot(fpr, tpr, label=f'ROC-kurve (AUC = {auc:.2f})')
plt.plot([0, 1], [0, 1], 'k--', label='Tilfældig model')
plt.xlabel('Falsk Positiv Rate')
plt.ylabel('Sand Positiv Rate')
plt.title('ROC-kurve')
plt.legend()
plt.tight_layout()
plt.savefig('./graphics/PD_ROC_curve.png')

# Krydstjekker med Somers' D
print('Somers D')
somersd_unbinned = somersd(y_true, y_scores).statistic
print(f'Somers D: {somersd_unbinned:.2f}')
print(f'Modsvarende en AUC på {0.5 + somersd_unbinned/2:.2f}')

# Beregner en (groft) binned udgave
pd_bin_edges = [0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
pd_bins = np.digitize(y_scores, pd_bin_edges)  # Subtract 1 to make bins 0-index
somersd_binned = somersd(y_true, pd_bins).statistic
print('Somers D (grov binning)')
print(f'Somers D (binned): {somersd_binned:.2f}')
print(f'Modsvarende en AUC på {0.5 + somersd_binned/2:.2f}')

# Tager en finere binning
pd_bin_edges = np.linspace(0, 1, 100)
pd_bins = np.digitize(y_scores, pd_bin_edges)  # Subtract 1 to make bins 0-index
somersd_binned = somersd(y_true, pd_bins).statistic
print('Somers D (fin binning)')
print(f'Somers D (binned): {somersd_binned:.2f}')
print(f'Modsvarende en AUC på {0.5 + somersd_binned/2:.2f}')

# OK, det her viser, at binning ikke er lige meget...

# Rangordning af variablen:
somersd_rank = somersd(y_true,df_pd.variabel).statistic
print(f'Somers D (variabel): {somersd_rank:.2f}')
print(f'Modsvarende en AUC på {0.5 + somersd_rank/2:.2f}')
