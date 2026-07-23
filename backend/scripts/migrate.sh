#!/bin/bash
set -e

cd "$(dirname "$0")/.."

export PYTHONPATH="${PYTHONPATH}:$(pwd)"

alembic upgrade head
