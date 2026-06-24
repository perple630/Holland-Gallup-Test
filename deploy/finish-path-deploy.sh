#!/usr/bin/env bash
set -e
CONF=/etc/nginx/sites-enabled/schedule.conf
MARKER='include /etc/nginx/snippets/holland-gallup-locations.conf;'
if ! grep -q "$MARKER" "$CONF"; then
  sudo sed -i "\$i\\    $MARKER" "$CONF"
fi
sudo rm -f /etc/nginx/sites-enabled/holland-gallup.conf
sudo cp /srv/holland-gallup/deploy/holland-gallup-locations.conf /etc/nginx/snippets/holland-gallup-locations.conf
sed -i 's|:8081|:8080|g' /srv/holland-gallup/deploy/.env
cd /srv/holland-gallup/frontend
VITE_BASE_PATH=/holland-gallup/ npm run build
sudo nginx -t
sudo systemctl reload nginx
sudo systemctl restart holland-gallup.service
echo DONE
