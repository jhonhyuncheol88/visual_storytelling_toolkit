#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ShotCanvas - AI 영상 제작 도구
macOS/Windows 응용프로그램으로 패키징하기 위한 진입점
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# src 폴더를 Python 경로에 추가
src_dir = os.path.join(current_dir, "src")
if os.path.exists(src_dir):
    sys.path.insert(0, src_dir)

# ShotCanvas 애플리케이션 실행
from cinescribe.app import main

if __name__ == "__main__":
    main()


