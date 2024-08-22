from typing import Any


def make_log_config(debug: bool) -> dict[str, Any]:
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] - %(message)s (%(filename)s:%(lineno)d)',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG' if debug else 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {},
    }

    if debug:
        config['loggers'] = {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
            }
        }
    else:
        config['loggers'] = {
            '': {
                'handlers': ['console'],
                'level': 'WARNING',
            },
            'translation_service': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False
            }
        }
    return config


__all__ = [
    'make_log_config'
]
