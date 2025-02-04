import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt
from scipy.stats import somersd

# Indlæser data
df_lgd = pd.read_csv('data/LGD_portefoelje.csv')

################################
# CR

# True labels (defaults)
y_true = df_lgd['cure']

# Estimerede sandsynligheder
y_scores = df_lgd['CR']

# Beregner ROCkurve
fpr, tpr, thresholds = roc_curve(y_true, y_scores)

# AUC
auc = roc_auc_score(y_true, y_scores)

# Plotter ROCkurve
plt.figure(figsize=(6, 4))
plt.plot(fpr, tpr, label=f'ROC-kurve (AUC = {auc:.4f})')
plt.plot([0, 1], [0, 1], 'k--', label='Tilfældig model')
plt.xlabel('Falsk Positiv Rate')
plt.ylabel('Sand Positiv Rate')
plt.title('ROC-kurve')
plt.legend()
plt.tight_layout()
plt.savefig('./graphics/CR_ROC_curve.png')


# Krydstjekker med Somers' D
print('Somers D')
somersd_unbinned = somersd(y_true, y_scores).statistic
print(f'Somers D: {somersd_unbinned:.4f}')
print(f'Modsvarende en AUC på {0.5 + somersd_unbinned/2:.4f}')

################################
# LGD

# Inddeler i intervaller
lgd_bin_edges = [0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
df_lgd['lgd_real_bins'] = np.digitize(df_lgd['LGD_REAL'], lgd_bin_edges)
df_lgd['lgd_bins'] = np.digitize(df_lgd['LGD'], lgd_bin_edges)

print(f'Somers\' D for LGD med realiseret LGD som uafhængig variabel: {somersd(df_lgd.lgd_real_bins, df_lgd.lgd_bins).statistic:4f}')

# LGL
print(f'Somers\' D for LGL med realiseret LGL som uafhængig variabel: {somersd(df_lgd[df_lgd.cure==0].lgd_real_bins, df_lgd[df_lgd.cure==0].lgd_bins).statistic:4f}')


pass