#!/bin/bash

# tests 디렉토리의 모든 테스트(pytest 기반) 실행

if ! command -v pytest &> /dev/null
then
    echo "pytest가 설치되어 있지 않습니다. 먼저 'pip install pytest'로 설치해주십시오."
    exit 1
fi

# 프로젝트 루트에서 실행해야 상대경로 문제 없음
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$SCRIPT_DIR"

pytest tests 