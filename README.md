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

# NWD — MediaWiki DevOps Project

Развёртывание MediaWiki с Nginx, MariaDB и системой мониторинга (Prometheus + Grafana + cAdvisor). Проект полностью контейнеризирован через Docker Compose, данные сохраняются в томах.

## Стек технологий

| Сервис      | Назначение                  | Порт      |
|-------------|-----------------------------|-----------|
| MediaWiki   | Движок вики                 | 80 (через Nginx) |
| Nginx       | Обратный прокси             | 80        |
| MariaDB     | База данных                 | 3306 (внутренний) |
| Prometheus  | Сбор метрик                 | 9090      |
| Grafana     | Визуализация метрик         | 3000      |
| cAdvisor    | Мониторинг контейнеров      | 8081      |

## Быстрый запуск

```bash
git clone https://github.com/uplink0/NWD.git
cd NWD
docker compose up -d
Первичная настройка MediaWiki
Открой http://localhost

Пройди веб-установку. Данные для подключения к БД указаны в docker-compose.yml в секции mediawiki-db → environment:

Хост базы данных: mediawiki-db

Имя базы данных: mediawiki

Пользователь и пароль: см. переменные MYSQL_USER и MYSQL_PASSWORD в docker-compose.yml

Префикс таблиц: оставь пустым

После завершения установки скачай файл LocalSettings.php

Помести его в корень проекта (NWD/LocalSettings.php)

Подключение LocalSettings.php
Открой docker-compose.yml

Найди секцию mediawiki-app → volumes

Раскомментируй строку:

yaml
# Было:
# - ./LocalSettings.php:/var/www/html/LocalSettings.php

# Стало:
- ./LocalSettings.php:/var/www/html/LocalSettings.php
Перезапусти контейнер:

bash
docker compose up -d mediawiki-app
Настройка Grafana
Открой http://localhost:3000 (логин/пароль по умолчанию: admin/admin, можно сменить в docker-compose.yml → GF_SECURITY_ADMIN_USER и GF_SECURITY_ADMIN_PASSWORD)

Добавь источник данных:

Connections → Data sources → Add data source → Prometheus

Prometheus server URL: http://prometheus:9090

Нажми Save & test

Импортируй дашборд для мониторинга контейнеров:

+ → Import dashboard

Введи ID дашборда: 19792

Выбери созданный Prometheus data source

Нажми Import

Другие полезные дашборды Grafana
ID	Описание
14282	Docker and system monitoring (альтернативный)
193	Docker monitoring (базовый)
8321	Docker monitoring with node selection
Найти другие дашборды: https://grafana.com/grafana/dashboards

Сохранность данных
Все данные сохраняются в именованных томах Docker:

db_data — база данных MediaWiki (статьи, пользователи)

mediawiki_data — загруженные файлы и изображения

prometheus_data — метрики Prometheus

grafana_data — настройки и дашборды Grafana

Чтобы полностью сбросить данные:

bash
docker compose down -v
Структура проекта
text
NWD/
├── docker-compose.yml    # Оркестрация всех сервисов
├── nginx/
│   └── default.conf      # Конфигурация обратного прокси
├── prometheus/
│   └── prometheus.yml    # Конфигурация сбора метрик
├── .gitignore            # Исключение конфиденциальных файлов
└── README.md             # Документация проекта
Важно: LocalSettings.php не хранится в репозитории (добавлен в .gitignore), так как содержит пароли от базы данных.