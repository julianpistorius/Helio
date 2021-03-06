from controller_exceptions import ControllerImportError
from settings import COMPONENT_DIRECTORIES


def get_controller_from_module_path(module_name):
    for path in COMPONENT_DIRECTORIES:
        mod = None

        module_final = module_name.split('.')[-1]

        namespace = '%s.%s.%s' % (path, module_name, module_final)
        try:
            mod = __import__(namespace, globals(), locals(), "Controller")
            break
        except ImportError:
            pass

    if mod is not None:
        return mod.Controller
    else:
        raise ControllerImportError(
            "Can't import '%s' controller. Searched in the following directories: %s" % (
                module_name,
                ", ".join(COMPONENT_DIRECTORIES),
            )
        )


def import_controllers(*args):
    """
    Return either a single controller Class, if one controller name arg is passed,
    or a dictionary of controller Classes, if multiple controller names are passed.
    """
    controllers = {}

    if len(args) == 1:
        return get_controller_from_module_path(args[0])

    for module_name in args:
        controllers[module_name] = get_controller_from_module_path(module_name)

    return controllers


def init_controller(component_name, *args, **kwargs):
    """
    Initialise and return a controller from component_name, with given *args and **kwargs.
    """
    return import_controllers(component_name)(*args, **kwargs)
