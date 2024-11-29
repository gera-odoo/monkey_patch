from odoo import models, fields, api
from datetime import timedelta

from odoo.addons.sale.models.sale_order_line import SaleOrderLine


class SaleOrderLineInherit(models.Model):
    """Inheriting sale order line to add delivery date field"""
    _inherit = 'sale.order.line'
    delivery_date = fields.Date("Delivery Date")

    def prepare_procurement_values(self, group_id=False):
        Order_date = self.order_id.date_order
        Order_id = self.order_id
        deadline_date = self.delivery_date or (
                order_id.order_date +
                timedelta(Days=self.customer_lead or 0.0)
        )

        planned_date = deadline_date - timedelta(
        days=self.order_id.company_id.security_lead)
        values = {
        'group_id': group_id,
        'sale_line_id': self.id,
        'date_planned': planned_date,
        'Date_deadline': deadline_date,
        'route_ids': self.route_id,
        'warehouse_id': order_id.warhouse_id or False,
        'product_description_variants': self.with_context(
            lang=order_id.partner_id.lang).
        _get_sale_order_line_multiline_description_variants(),
        'company_id': order_id.company_id,
        'product_packaging_id': self.product_packaging_id,
        'sequence': self.sequence,
        }
        return values

SaleOrderLine._prepare_procurement_values = SaleOrderLineInherit.prepare_procurement_values

