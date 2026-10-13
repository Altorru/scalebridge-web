# Contributing / Contribuer

Small, focused changes to this static web edition are welcome. Run `python3 tools/check.py`, then serve locally and check 360 px, tablet and desktop, keyboard focus, readable labels, light/dark/system themes and downloads. The fictional results must remain identified as fixed examples. No health data, participant records, credentials or native Android artifacts in issues or pull requests.

Regenerate downloads with `python3 tools/package_downloads.py` after changing fixtures, assets or notices. Regenerate the file inventory with `python3 tools/check.py --write-manifest`; review the changed paths and hashes. Keep existing third-party attribution. For a bug report, state the page, browser, steps and expected/actual behaviour using fictional examples only.

Ce dépôt est limité au web statique. Ne pas ajouter de collecte de mesures, paiement, compatibilité fabricant ou affirmation de résultats utilisateurs sans périmètre explicite. Conserver les licences et tester les téléchargements et l’accessibilité.
