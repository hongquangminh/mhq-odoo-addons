# -*- coding: utf-8 -*-
# Copyright (C) 2017 Hom Nay Code Gi Blog (<https://homnaycodegi.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoo

class AssetsBundle(object):

    def save_attachment(self, type, content, inc=None):
        with odoo.api.Environment.manage():
            with odoo.registry(self.env.cr.dbname).cursor() as new_cr:
                new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                assert type in ('js', 'css')
                ira = new_env['ir.attachment']
                fname = '%s%s.%s' % (
                    self.name,
                    ('' if inc is None else '.%s' % inc),
                    type
                )
                mimetype = 'application/javascript' if type == 'js' else 'text/css'
                values = {
                    'name': "/web/content/%s" % type,
                    'datas_fname': fname,
                    'mimetype': mimetype,
                    'res_model': 'ir.ui.view',
                    'res_id': False,
                    'type': 'binary',
                    'public': True,
                    'datas': content.encode('utf8').encode('base64'),
                }
                attachment = ira.sudo().create(values)
                url = '/web/content/%s-%s/%s' % (attachment.id, self.version, fname)
                values = {
                    'name': url,
                    'url': url,
                }
                attachment.write(values)

                if new_env.context.get('commit_assetsbundle') is True:
                    new_env.cr.commit()
                self.with_env(new_env).clean_attachments(type)
                return attachment
