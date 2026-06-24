# 服务器部署说明

## 当前生产环境

| 项目 | 路径 | 端口/路径 | 说明 |
|------|------|-----------|------|
| alevelinfo | — | `:80` | 现有 Node 项目，未改动 |
| schedule | `/srv/schedule` | `:8080/` | 现有排课系统，未改动 |
| **holland-gallup** | `/srv/holland-gallup` | `:8070/` | 本项目（独立端口） |

- 后端：`127.0.0.1:8001`（systemd: `holland-gallup.service`）
- 前端：Nginx 根路径部署，无需 `VITE_BASE_PATH`

## 访问地址

http://42.193.112.229:8070/

演示账号见部署文档；学生请注册，教师/管理员由系统分配。

## 预设高级账号（import_data 种子）

| 用户名 | 角色 | 初始密码 |
|--------|------|----------|
| admin | 管理员 | `Hg@Admin2026!xK9` |
| supervisor | 管理员 | `Hg@Supervisor2026!vQ7` |
| teacher | 教师 | `Hg@Teacher2026!mP4` |
| student | 演示学生 | `Student@2026!demo` |

## 更新部署（本机 PowerShell）

```powershell
$archive = "$env:TEMP\holland-gallup-deploy.tgz"
Set-Location "d:\UESR\Desktop\Holland-Gallup-Test"
tar -czf $archive --exclude=node_modules --exclude=.git --exclude=backend/venv --exclude=frontend/dist --exclude=.obsidian --exclude=backend/data/*.db .
scp -i "$env:USERPROFILE\.ssh\alevelinfo_ed25519" $archive ubuntu@42.193.112.229:/tmp/holland-gallup-deploy.tgz
ssh -i "$env:USERPROFILE\.ssh\alevelinfo_ed25519" ubuntu@42.193.112.229 "tar xzf /tmp/holland-gallup-deploy.tgz -C /srv/holland-gallup"
ssh -i "$env:USERPROFILE\.ssh\alevelinfo_ed25519" ubuntu@42.193.112.229 "bash -lc 'cd /srv/holland-gallup/backend && .venv/bin/pip install -r requirements.txt && .venv/bin/python -m app.import_data'"
ssh -i "$env:USERPROFILE\.ssh\alevelinfo_ed25519" ubuntu@42.193.112.229 "bash -lc 'cd /srv/holland-gallup/frontend && npm ci && npm run build'"
ssh -i "$env:USERPROFILE\.ssh\alevelinfo_ed25519" ubuntu@42.193.112.229 "sudo systemctl restart holland-gallup.service"
```

## 关键文件

- `deploy/holland-gallup.service` — systemd 单元
- `deploy/holland-gallup-locations.conf` — Nginx 子路径片段
- `deploy/schedule-with-holland.conf` — schedule 站点完整配置（含 include）
