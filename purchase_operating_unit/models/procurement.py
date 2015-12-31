# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, models
from openerp.tools.translate import _
from openerp.exceptions import UserError


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    @api.one
    @api.constrains('operating_unit_id', 'purchase_line_id')
    def _check_purchase_order_operating_unit(self, cr, uid, ids, context=None):
        purchase = self.purchase_line_id.purchase_id
        if purchase and\
                self.purchase.operating_unit_id !=\
                self.location_id.operating_unit_id:
            raise UserError(_('Configuration error!\nThe Quotation / Purchase\
            Order and the Procurement Order must belong to the\
            same Operating Unit.'))

    @api.multi
    def _prepare_purchase_order(self, partner):
        res = super(ProcurementOrder, self)._prepare_purchase_order(partner)
        operating_unit = self.location_id.operating_unit_id
        if operating_unit:
            res.update({
                'operating_unit_id': operating_unit.id,
                'requesting_operating_unit_id': operating_unit.id
            })
        return res