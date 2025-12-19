#!/bin/bash
# Schnellstart-Skript für Besemer-MCMC Analyse

echo "=== Besemer-MCMC Analyse ==="
echo ""

# Prüfe Python
if ! command -v python3 &> /dev/null; then
    echo "Fehler: Python3 nicht gefunden"
    exit 1
fi

# Installiere Dependencies (falls nötig)
echo "Prüfe Dependencies..."
pip3 install -q -r requirements.txt

# Führe Analyse aus
echo ""
echo "Starte Analyse..."
echo ""

python3 main.py \
    --beta 296 \
    --resolution 100 \
    --h0-min 60 \
    --h0-max 80 \
    --om-min 0.2 \
    --om-max 0.4 \
    --output ./results

echo ""
echo "=== Analyse abgeschlossen ==="
echo "Ergebnisse: ./results/"
echo "Plots: ./results/plots/"
