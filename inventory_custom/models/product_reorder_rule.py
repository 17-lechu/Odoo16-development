from odoo import models, fields


class ProductReorderRule(models.Model):
    _name = 'product.reorder.rule'

    name = fields.Char(string='Name')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    minimum_stock = fields.Float(string='Minimum Stock')
    maximum_stock = fields.Float(string='Maximum Stock')
    reorder_quantity = fields.Float(string='Reorder Quantity')
    lead_time = fields.Integer(string='Lead Time (Days)')

    def check_stock_levels(self):
        for rule in self.env['product.reorder.rule'].search([]):
            if rule.product_id.qty_available < rule.minimum_stock:
                self.generate_replenishment_orders(rule)

    def generate_replenishment_orders(self, rule):
        if rule.product_id.seller_ids:
            for line in rule.product_id.seller_ids:
                if rule.lead_time <= line.delay:
                    replenishment = self.env['stock.warehouse.orderpoint'].create({
                        'product_id': rule.product_id.id,
                        'product_min_qty': rule.minimum_stock,
                        'product_max_qty': rule.maximum_stock,
                    })
                    replenishment.action_replenish()


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('approved', 'Approved'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    def action_approve_order(self):
        self.write({'state': 'approved'})
