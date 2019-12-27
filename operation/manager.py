import threading

from frameworks.utils.log import Log


class OperationManager(object):
    """docstring for OperationManager"""

    _instance_lock = threading.Lock()

    def __init__(self):
        super(OperationManager, self).__init__()

        self._operation_map = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(OperationManager, "_instance"):
            with OperationManager._instance_lock:
                if not hasattr(OperationManager, "_instance"):
                    OperationManager._instance = object.__new__(cls)
        return OperationManager._instance

    def get_operation(self, operation_name):
        operation = None

        try:
            operation_full_path = 'operations.%s' % operation_name
            module_t = __import__(operation_full_path)
            opt_module = getattr(module_t, operation_name)
            c = getattr(opt_module, operation_name.title())
            operation = object.__new__(c)
        except Exception as e:
            Log.e(e)
            operation = None

        return operation
