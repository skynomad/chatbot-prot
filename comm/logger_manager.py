import logging

class LoggerManager:
    """
    로거를 관리하는 클래스. 글로벌 영역에서 로거를 재사용할 수 있도록 설정.
    """
    _loggers = {}

    @staticmethod
    def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
        """
        로거를 생성하거나 기존 로거를 반환.

        Args:
            name (str): 로거의 이름.
            level (int): 로깅 레벨 (기본값: INFO).

        Returns:
            logging.Logger: 설정된 로거 객체.
        """
        if name not in LoggerManager._loggers:
            logger = logging.getLogger(name)
            if not logger.handlers:  # 중복 핸들러 방지
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                logger.addHandler(handler)
                logger.setLevel(level)
            LoggerManager._loggers[name] = logger
        return LoggerManager._loggers[name]