import threading

from utils.log import Log


class PluginManager(object):
    """docstring for PluginManager"""

    _instance_lock = threading.Lock()

    def __init__(self):
        super(PluginManager, self).__init__()

        self._plugin_map = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(PluginManager, "_instance"):
            with PluginManager._instance_lock:
                if not hasattr(PluginManager, "_instance"):
                    PluginManager._instance = object.__new__(cls)
        return PluginManager._instance

    def get_plugin(self, plugin_name):
        plugin = None

        try:
            plugin_full_path = 'plugins.%s' % plugin_name
            module_t = __import__(plugin_full_path)
            opt_module = getattr(module_t, plugin_name)
            c = getattr(opt_module, plugin_name.title())
            plugin = object.__new__(c)
        except Exception as e:
            Log.e(e)
            plugin = None

        return plugin
