# Read-only DevOps Diagnostic Agent

Локальный диагностический агент для Ubuntu. Собирает ограниченные read-only данные Linux, Kubernetes и контейнеров, выявляет типовые симптомы и передаёт очищенные результаты локальной модели Ollama. Команды из ответа модели никогда не исполняются.

## Требования

- Ubuntu 22.04/24.04, Python 3.10+.
- Опционально: kubectl с kubeconfig и Ollama.
- Запускать только от обычного пользователя, не от root.
- Не добавлять пользователя в группу docker ради агента: доступ к Docker socket фактически даёт root-полномочия.
- Для Kubernetes использовать отдельный контекст с RBAC только на чтение. Не выдавать права на Secrets и изменение ресурсов.

## Установка

    sudo apt update
    sudo apt install -y python3 python3-venv git
    git clone --branch feature/read-only-devops-agent https://github.com/uplink0/NWD.git
    cd NWD/diagnostic-agent
    python3 -m venv .venv
    source .venv/bin/activate

Python-зависимостей из PyPI нет: используется стандартная библиотека.

## Запуск

Только Linux:

    python devdiag.py diagnose --target host --no-llm

Kubernetes:

    python devdiag.py diagnose --target kubernetes

Контейнеры:

    python devdiag.py diagnose --target containers

Все доступные проверки:

    python devdiag.py diagnose --target all

Отчёты создаются в reports/ в форматах Markdown и JSON.

## Локальная модель Ollama (необязательно)

Установите Ollama по официальной инструкции: https://ollama.com/download

    ollama pull qwen2.5:3b

Убедитесь, что Ollama доступна на http://127.0.0.1:11434. Затем:

    OLLAMA_MODEL=qwen2.5:3b python devdiag.py diagnose --target all

Переменные окружения: OLLAMA_URL (по умолчанию http://127.0.0.1:11434), OLLAMA_MODEL (по умолчанию qwen2.5:3b).

## Проверка прав Kubernetes

    kubectl config current-context
    kubectl auth can-i list pods --all-namespaces
    kubectl auth can-i list events --all-namespaces
    kubectl auth can-i get secrets --all-namespaces
    kubectl auth can-i create deployments --all-namespaces

Для выделенного контекста последние две проверки должны вернуть no. Сам агент не запрашивает Secrets и не запускает операции изменения.

## Безопасность и ограничения

- Команды заданы в исходном коде как фиксированные массивы аргументов; shell не используется.
- Ответ LLM — только текст отчёта. Команды из него не исполняются.
- Вывод ограничен по размеру и очищается от распространённых форматов секретов.
- Приложен минимальный набор проверок; автоматического чтения логов приложений нет, чтобы снизить риск утечки секретов.
- Это MVP, не сертифицированная security boundary. Перед production проверьте права пользователя, kubeconfig и доступ к Docker socket.
- Агент ничего не исправляет. Все предлагаемые команды нужно проверить и запускать вручную.
