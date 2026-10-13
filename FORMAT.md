> Cette édition web affiche un exemple fixe. Ce document décrit les données de référence du candidat ; aucun moteur d’import Android n’est inclus. / This web edition displays a fixed fixture; the native importer is not included.

# Format local v1 / Local format v1

Les exemples du dossier `examples/` sont fictifs. / All example files are fictional.

## CSV d'entrée / Input CSV

UTF-8 (BOM accepté), virgule ou point-virgule, en-tête obligatoire avec 2–30 colonnes nommées uniques. 1 Mio et 10 000 lignes maximum. Champs CSV entre guillemets, guillemets doublés et retours CRLF acceptés. Un fichier structurellement malformé est rejeté entièrement ; les lignes à valeur invalide sont listées et exclues après confirmation explicite.

UTF-8 (optional BOM), comma or semicolon, mandatory header with 2–30 unique named columns. Maximum 1 MiB and 10,000 data rows. Quoted fields, doubled quotes and CRLF supported. Structural errors reject the whole file; invalid data rows are listed and excluded after explicit confirmation.

- Date : `2026-10-07`, `2026-10-07T08:00:00`, `2026-10-07 08:00:00`, `2026-10-07T08:00:00+02:00`, `2026-10-07T06:00:00Z`. Pas de date `07/10/2026`, timestamp Unix ou conversion implicite jour/mois. Dates 1900–2100.
- Date-only means midnight in the selected IANA timezone. Local times use the selected timezone, initially the device timezone. Offset/Z timestamps override that choice. Daylight-saving gaps or overlaps require an explicit offset; the importer never silently chooses one.
- Poids : unité explicite kg ou lb. `1 lb = 0.45359237 kg`, arrondi HALF_UP à 0,001 kg, plage 1–500 kg. La précision conservée définit l'équivalence des doublons.
- Weight: explicit kg/lb selection. Converted and rounded to 0.001 kg; 1–500 kg bounds. No thousands separators, exponents, NaN or stone values.
- Masse grasse : facultative, 0–100 %, point ou virgule décimale, suffixe `%` accepté, vide = absent. `0.18` signifie 0,18 %, pas 18 %.
- Decimal commas require semicolon-separated CSV or a quoted comma-separated field. Columns cannot share a mapping.

## Déduplication / Deduplication

Clé = instant UTC à la précision d'origine. Instant et valeurs normalisées égaux = doublon, même sur retry. Même instant et valeurs différentes (y compris masse grasse absente vs renseignée) = conflit, première valeur conservée. Aucun écrasement automatique. Le bilan indique les nombres de conflits ; corriger le CSV puis, si nécessaire, supprimer et réimporter un historique maîtrisé. Deux instants distincts le même jour restent deux mesures.

Key is the original-precision UTC instant. Equal normalized values are duplicates. Different values at the same instant are conflicts and the first saved value wins. No automatic replacement. Different times on the same date are kept. No provider identifier or source filename is retained.

## Export

CSV : `date,weight_kg,body_fat_percent`, UTC ISO, points décimaux, CRLF ; réimportable en kg, mêmes colonnes. JSON : `{ "schema_version": 1, "unit": "kg", "measurements": [{ "date": "...Z", "weight_kg": 78.2, "body_fat_percent": null }] }`. JSON est un format de sortie, pas un format d'entrée de la v1. Aucun format ne garantit l'import par une plateforme tierce.

CSV exports are round-trippable in ScaleBridge. JSON is export-only in v1. No destination compatibility is claimed. Store limit is 50,000 measurements; history shows the latest 200, exports contain all. Journal keeps the latest 100 confirmed operations.

Un export dépassant 10 000 lignes ou 1 Mio doit être fractionné en CSV avec en-tête pour être réimporté. / An export exceeding input limits must be split into CSVs with headers before reimport.
