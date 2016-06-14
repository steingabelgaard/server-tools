# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
<<<<<<< HEAD
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import os
from openerp import http
from openerp.http import request


class Letsencrypt(http.Controller):
    @http.route('/.well-known/acme-challenge/<filename>', auth='none')
    def acme_challenge(self, filename):
        try:
            with file(
                os.path.join(request.env['letsencrypt'].get_challenge_dir(),
                             filename)
            ) as challenge:
                return challenge.read()
=======
# © 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import os
from openerp import http
from openerp.http import request
from ..models.letsencrypt import get_challenge_dir


class Letsencrypt(http.Controller):
    @http.route('/.well-known/acme-challenge/<filename>', auth='none')
    def acme_challenge(self, filename):
        try:
            with file(os.path.join(get_challenge_dir(), filename)) as key:
                return key.read()
>>>>>>> refs/remotes/dreispt/8.0-search
        except IOError:
            pass
        return request.not_found()
