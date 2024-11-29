# -*- coding: utf-8 -*-

from . import controllers
from . import models
from odoo import api, SUPERUSER_ID


def _new_uninstall(env):
    def update_module(xmlid):
        act = env.ref(xmlid, raise_if_not_found=False)
        if act:
            act.button_upgrade()

    update_module('base.module_sale_management')


def uninstall_hook(cr, registry):
    """Uninstall hook to perform cleanup actions."""
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Remove custom configurations or temporary data
    env['ir.config_parameter'].sudo().set_param('custom_param', False)

    # Call the helper function to trigger module upgrade
    _new_uninstall(env)
