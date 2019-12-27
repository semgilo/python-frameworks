import threading

from frameworks.utils.log import Log


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
            plugin_full_path = 'plugins.%s.%s' % (plugin_name, plugin_name)
            module_t = __import__(plugin_full_path)
            opt_module = getattr(module_t, plugin_name)
            opt_module = getattr(opt_module, plugin_name)
            classname = ""
            names = plugin_name.split("_")
            for name in names:
                classname += name.title()

            c = getattr(opt_module, classname)
            plugin = object.__new__(c)
            plugin.__init__()

        except Exception as e:
            Log.e(e)
            plugin = None

        return plugin
