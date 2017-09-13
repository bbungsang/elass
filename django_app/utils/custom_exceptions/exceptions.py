__all__ = (
    'CustomIndexError',
)


class CustomIndexError(Exception):
    def __init__(self, key):
        self.msg = '{} 파라미터의 수가 맞지 않습니다'.format(key)

    def __str__(self):
        return self.msg