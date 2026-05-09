# NWD — MediaWiki DevOps Project

Развёртывание MediaWiki с Nginx, MariaDB и системой мониторинга.

## Стек
- **MediaWiki** — движок вики
- **Nginx** — обратный прокси
- **MariaDB** — база данных
- **Prometheus** — сбор метрик
- **Grafana** — визуализация метрик
- **cAdvisor** — мониторинг контейнеров

## Запуск
```bash
docker compose up -d
