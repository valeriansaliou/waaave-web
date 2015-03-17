"""
Forms defaults
Contains commonly-used form settings
"""

DEFAULT_MAX = 80
URL_MAX = 2000

PWD_LENGTH_MIN = 6
PWD_LENGTH_MAX = 42

PATTERN_EMAIL = '.+\@.+\..+'
PATTERN_PWD = '.{' + str(PWD_LENGTH_MIN) + ',' + str(PWD_LENGTH_MAX) + '}'
PATTERN_USERNAME = '.+'
