# Eure Berliner Autopflege

Website mit November-Aktion 2026. Veröffentlichung über GitHub Actions auf Hetzner.

Die Website liegt in `dist/`; `generate.py` erzeugt die Seiten. Der Workflow verwendet `HETZNER_HOST`, `HETZNER_USER`, `HETZNER_PASSWORD` (alternativ `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`) und optional `HETZNER_PORT` sowie die Repository-Variable `DEPLOY_PATH`. `SITE_BASE_URL` setzt die öffentliche Domain.
