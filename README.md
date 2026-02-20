## projet_monitoring_en_temp_reel

## Objectif

Créer un dashboard interactif et temps réel dans Looker Studio, alimenté par Google Sheets, afin de visualiser les performances système (CPU, RAM, Disk, Network, Temp) et détecter les anomalies.

## Technologies

- Python (psutil)
- Google Sheets API
- Looker Studio
- Google Cloud Console (OAuth)

## Fonctionnement

1. Un script Python collecte les métriques système.
2. Les données sont envoyées automatiquement vers Google Sheets.
3. Looker Studio exploite la feuille pour afficher :
   - Des visualisations historiques (Time Series)
   - Des indicateurs temps réel (Scorecards & Gauge)
   - Un statut CPU (HIGH / MEDIUM / NORMAL)

Auto-refresh activé toutes les 15 minutes.

## Liens

**Google Sheet :**  
[https://YOUR_GOOGLE_SHEET_LINK ](https://docs.google.com/spreadsheets/d/1Cb5tZe6VZMQxJ_H0XJQbBceqpSQj8XMz5aRCsNUWgyQ/edit?usp=sharing) 

**Dashboard Looker Studio :**  
[https://YOUR_LOOKER_STUDIO_LINK  ](https://lookerstudio.google.com/s/iU5noa8fFUc)

## Aperçu

<img width="828" height="618" alt="Capture d&#39;écran 2026-02-20 140152" src="https://github.com/user-attachments/assets/f45d2df4-282e-4add-bd36-62df4c412e41" />

