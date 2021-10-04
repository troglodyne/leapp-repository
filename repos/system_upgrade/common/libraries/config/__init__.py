from leapp.libraries.stdlib import api


def get_env(name, default=None):
    """Return Leapp environment variable value if matched by name."""
    for var in api.current_actor().configuration.leapp_env_vars:
        if var.name == name:
            return var.value
    return default


def get_all_envs():
    """Return all Leapp environment variables (both name and value)."""
    return api.current_actor().configuration.leapp_env_vars


def get_product_type(sys_type):
    """
    Get expected product type (ga/beta/htb) of the chosen sys type.

    By default, expected product type is 'ga'. It can be changed using these envars:
        LEAPP_DEVEL_SOURCE_PRODUCT_TYPE
        LEAPP_DEVEL_TARGET_PRODUCT_TYPE
    which can set the product type of chosen system (source/target) to one of
    valid product types: ga/beta/htb.

    Raise ValueError when specified sys_type or set product_type is invalid.

    :param sys_type: choose system for which to get the product type: 'source' or 'target'
    :type sys_type: str
    :return: 'ga' (default), 'htb', 'beta'
    :rtype: str
    """
    if sys_type == 'source':
        envar = 'LEAPP_DEVEL_SOURCE_PRODUCT_TYPE'
    elif sys_type == 'target':
        envar = 'LEAPP_DEVEL_TARGET_PRODUCT_TYPE'
    else:
        raise ValueError('Given invalid sys_type. Valid values: source/target')
    val = get_env(envar, '').lower()
    if not val:
        return 'ga'
    if val in ('beta', 'htb', 'ga'):
        return val
    raise ValueError('Invalid value in the {} envar. Possible values: ga/beta/htb.'.format(envar))


def get_target_product_channel(default='ga'):
    """
    Get target product channel specified when running the IPU or default if no channel was specified.

    The target channel can be specified via:
        - Using the environment variable LEAPP_DEVEL_TARGET_PRODUCT_TYPE (devel variable with higher priority than
        other any way of specifying target channel).
        - Using the environment variable LEAPP_TARGET_PRODUCT_CHANNEL
        - Using the '--channel' option when runnning leapp preupgrade/upgrade

    :param default: Value to be returned if no target product type has been specified when running leapp.
    :type default: str
    :returns: The user-specified target channel or default if no channel was specified.
    :rtype: str
    """

    devel_target_product_type = gen_env('LEAPP_DEVEL_TARGET_PRODUCT_TYPE')
    if devel_target_product_type:
        return devel_target_product_type

    target_product_channel = gen_env('LEAPP_TARGET_PRODUCT_CHANNEL')
    if target_product_channel:
        return target_product_channel

    return default
