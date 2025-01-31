# SomersDref
Referencekode til anvendelse af Somers' D

## Grundlæggende idé

Vi skal bruge Somers' D i mgange sammenhænge i fot hold til PD og LGD modeller. Således er det måske en god idé at have lidt eksempelkode i Python (og gerne SAS) der viser, hvordan man påtænker at gøre det.

## Scope

Liste af ting vi skal kunne beregne Somers' D for (og forklare hvad vi gør)

- PD
  - Rangordningsevne af PD-estimat
  - Rangordningsevne af enkeltvariable
- LGD
  - Rangordningsevne af CR
  - Rangordningsevne af enkeltvariable i CR
  - Rangordningsevne af LGL/LGD estimater
  - Rangordningsevne af enkeltvariable
 
Hvis vi kan lave et Pythonprogram der gennemløber eksempler på alt det her og koder det op, så har vi vel gjort vores kolleger en tjeneste.

Hvis vi sågar oversætter til SAS og bekræfter, at vi får det samme, så er vi vel golden.

## Status

### Porteføljebygger

`portefoeljebygger.py` bygger både en PD portefølje og en LGD portefølje.

#### PD portefølje

Per default genereres 10.000 kontakter med følgende information:
- PD
- En beskrivende variabel til Somers' D studier
- Misligholdsflag

Fordelingen af PD for porteføljen er vist i figuren nedenfor. Det ses, at mislighold typisk har højere PD.


![PD fordelinger](graphics/PD_portefoelje.png)

#### LGD portefølje

Per default genereres 10.000 kontakter med følgende information:
- CR: Estimeret cure rate
- LGL: Estimeret Loss Given Loss
- LGC: Estimeret Loss Given Cure
- LGD: Beregnet LGD $LGD = LGL \cdot (1 - CR) + LGC \cdot CR$
- cure: Cure flag
- cr_var: En beskrivende variabel til Somers' D studier
- LGD_REAL: Realiseret LGD

Et par beskrivende grafer:
![CR fordelinger](graphics/CR_fordeling.png)
![LGL fordelinger](graphics/LGL_fordeling.png)
![LGD fordelinger](graphics/LGD_fordelinger.png)

Der mangler nok stadig en beskrivende variabel eller to, men mon ikke vi kan komme i gang?