# -*- coding: utf-8 -*-
# © 2016 Daniel Reis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo import SUPERUSER_ID


class BaseModelExtend(models.AbstractModel):
    _inherit = 'base'
    
    @api.model
    @api.returns('self',
        upgrade=lambda self, value, args, offset=0, limit=None, order=None, count=False: value if count else self.browse(value),
        downgrade=lambda self, value, args, offset=0, limit=None, order=None, count=False: value if count else value.ids)
    def search(self, args, offset=0, limit=None, order=None, count=False):
        
        for i, cond in enumerate(args):
                    # fuzzy search: replace spaces with wildcards
                    if len(cond) == 3 and cond[1] == 'ilike' and isinstance(cond[2], str):
                        args[i] = cond[0], cond[1], cond[2].replace(' ', '%')
        
        return super(BaseModelExtend, self).search(args,offset=offset, limit=limit, order=order, count=count)
