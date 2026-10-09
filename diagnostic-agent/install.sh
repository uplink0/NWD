#!/usr/bin/env bash
set -euo pipefail

if [[ "$EUID" -eq 0 ]]; then
  echo "Не запускайте установщик от root. Запустите обычным пользователем."
  exit 1
fi

command -v python3 >/dev/null 2>&1 || {
  echo "Python 3 не найден. Установите: sudo apt install python3 python3-venv"
  exit 1
}

python3 -m venv .venv
echo "Готово. Активируйте окружение: source .venv/bin/activate"
echo "Проверка без LLM: python devdiag.py diagnose --target host --no-llm"
