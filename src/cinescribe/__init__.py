"""
ShotCanvas - AI 영상 제작 도구
cinescribe 패키지

AI 영상 제작을 위한 종합적인 도구 모음
"""

__version__ = "1.0.0"
__author__ = "ShotCanvas Team"
__description__ = "AI 영상 제작을 위한 시각적 스토리텔링 도구"

# 주요 패키지들을 import하여 사용자 편의성 제공
try:
    from . import views
    from . import service
    from . import repository
    from . import utils
    from . import domain
    from . import viewmodel
    from . import widgets
except ImportError:
    # 개발 환경에서 상대 import가 실패할 경우를 대비
    pass

__all__ = [
    'views',
    'service',
    'repository', 
    'utils',
    'domain',
    'viewmodel',
    'widgets'
]
