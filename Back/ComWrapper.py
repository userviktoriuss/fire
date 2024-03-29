import time
import logging

import comtypes
from comtypes.client import lazybind

_DELAY = 0.05  # Seconds.
_TIMEOUT = 60.0  # Seconds.


# TODO: здесь в 2+ местах надо ловить не все COMError, а только связанные с вызовом (мб не по имени, т.к. оно локале зависимо)
def _com_call_wrapper(f, *args, **kwargs):
    """
    Вспомогательная функция для ComWrapper.
    Выполняет повторные вызовы до тех пор, пока возникает
    исключение типа COMError, но не дольше заданного времени.
    """
    #
    args = [arg._wrapped_object if isinstance(arg, ComWrapper) else arg for arg in args]
    kwargs = dict([(key, value._wrapped_object)
                   if isinstance(value, ComWrapper)
                   else (key, value)
                   for key, value in dict(kwargs).items()])

    start_time = None
    while True:
        try:
            result = f(*args, **kwargs)
        except comtypes.COMError as e:
            print(e)
            # if e.strerror == 'Call was rejected by callee.':
            if start_time is None:
                start_time = time.time()
                logging.warning('Call was rejected.')

            elif time.time() - start_time >= _TIMEOUT:
                raise

            time.sleep(_DELAY)
            continue
        break

    if isinstance(result, lazybind.Dispatch) or callable(result):
        return ComWrapper(result)
    return result


class ComWrapper(object):
    """
    Обёртка для отлавливания ошибок при работе с COM.
    Адаптировано с https://stackoverflow.com/questions/3718037/error-while-working-with-excel-using-python.
    """

    def __init__(self, wrapped_object):
        assert isinstance(wrapped_object, comtypes.client.lazybind.Dispatch) or callable(wrapped_object)
        self.__dict__['_wrapped_object'] = wrapped_object

    def __getattr__(self, item):
        return _com_call_wrapper(self._wrapped_object.__getattr__, item)

    def __getitem__(self, item):
        return _com_call_wrapper(self._wrapped_object.__getitem__, item)

    def __setattr__(self, key, value):
        _com_call_wrapper(self._wrapped_object.__setattr__, key, value)

    def __setitem__(self, key, value):
        _com_call_wrapper(self._wrapped_object.__setitem__, key, value)

    def __call__(self, *args, **kwargs):
        return _com_call_wrapper(self._wrapped_object.__call__, *args, **kwargs)

    def __repr__(self):
        return 'ComWrapper<{}>'.format(repr(self._wrapped_object))


if __name__ == '__main__':
    pass
