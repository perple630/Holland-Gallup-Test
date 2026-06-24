#!/usr/bin/env bash
set -euo pipefail

APP_ROOT="/srv/holland-gallup"
DEPLOY_DIR="$APP_ROOT/deploy"

echo "[1/7] 准备目录..."
sudo mkdir -p "$APP_ROOT"
sudo chown -R ubuntu:ubuntu "$APP_ROOT"

echo "[2/7] 配置环境变量..."
if [ ! -f "$DEPLOY_DIR/.env" ]; then
  cp "$DEPLOY_DIR/env.example" "$DEPLOY_DIR/.env"
  SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(48))")
  sed -i "s|^SECRET_KEY=.*|SECRET_KEY=$SECRET|" "$DEPLOY_DIR/.env"
fi

echo "[3/7] 安装 Python 依赖..."
cd "$APP_ROOT/backend"
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

echo "[4/7] 初始化数据库..."
mkdir -p data
.venv/bin/python -m app.import_data

echo "[5/7] 构建前端..."
cd "$APP_ROOT/frontend"
npm ci
npm run build

echo "[6/7] 注册 systemd 服务..."
sudo cp "$DEPLOY_DIR/holland-gallup.service" /etc/systemd/system/holland-gallup.service
sudo systemctl daemon-reload
sudo systemctl enable holland-gallup.service
sudo systemctl restart holland-gallup.service

echo "[7/7] 配置 Nginx..."
sudo cp "$DEPLOY_DIR/holland-gallup.nginx.conf" /etc/nginx/sites-available/holland-gallup.conf
sudo ln -sf /etc/nginx/sites-available/holland-gallup.conf /etc/nginx/sites-enabled/holland-gallup.conf
sudo nginx -t
sudo systemctl reload nginx

echo "部署完成。"
echo "访问地址: http://$(curl -s ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}'):8081"
echo "演示账号: student/student123, teacher/teacher123"
