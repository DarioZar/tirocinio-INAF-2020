# Tirocinio INAF 2020
Modelli fluidodinamici con [Pluto].

## Sedov
Simulazione di una blast wave di Sedov-Taylor. Codice incluso tra gli esempi di [Pluto].

## Supernova
Simulazione della fase di espansione di Sedov per un SNR, in 2D, con simmetria cilindrica.
Contiene:
- varie run svolte con risoluzioni diverse (128x128, 256x256, 512x512, 1024x1024)
- `andamentoMassa.pdf`, generato con `tracker_analyze.py`, che mostra la massa delle regioni con più del 90% di materiale stellare
- `tracker_analyze.py`, che richiede `pyPLUTO`, `matplotlib` e `numpy`



[Pluto]: <http://plutocode.ph.unito.it/>