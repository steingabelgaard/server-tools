# -*- coding: utf-8 -*-
# © 2016 Daniel Reis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp import SUPERUSER_ID


class ModelExtended(models.Model):
    _inherit = 'ir.model'

    def _register_hook(self, cr, ids=None):

        def make_search():

            prefixes = ['=', '<', '>', '!']
            infixes = ['..']

            def can_expand(val, prefixes, infixes):
                return (any(str(val).startswith(x) for x in prefixes) or
                        any(x in str(val) for x in infixes))

            upgrade = lambda self, value, args, offset=0, limit=None, \
                             order=None, count=False: value if count else self.browse(value)
            downgrade = lambda self, value, args, offset=0, limit=None, \
                               order=None, count=False: value if count else value.ids

            @api.returns('self', upgrade=upgrade, downgrade=downgrade)
            def new_search(self, cr, user, args, offset=0, limit=None,
                           order=None, context=None, count=False):
                #_logger.info("New search")
                for i, cond in enumerate(args):
                    # fuzzy search: replace spaces with wildcards
                    if len(cond) == 3 and cond[1] == 'ilike':
                        args[i] = cond[0], cond[1], cond[2].replace(' ', '%')
                        #_logger.info("New search: %s", args[i])
                return new_search.origin(self, cr, user, args, offset=offset, limit=limit,
                                         order=order, context=context, count=count)
            return new_search

        if ids is None:
            ids = self.search(cr, SUPERUSER_ID, [])
        for model in self.browse(cr, SUPERUSER_ID, ids):
            Model = self.pool.get(model.model)
            if Model:
                Model._patch_method('search', make_search())
        return super(ModelExtended, self)._register_hook(cr)
