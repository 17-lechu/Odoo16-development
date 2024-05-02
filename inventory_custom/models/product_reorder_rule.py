from odoo import models, fields


class ProductReorderRule(models.Model):
    _name = 'product.reorder.rule'

    name = fields.Char(string='Name')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    minimum_stock = fields.Float(string='Minimum Stock')
    reorder_quantity = fields.Float(string='Reorder Quantity')
    lead_time = fields.Integer(string='Lead Time (Days)')
    partner_id = fields.Many2one('res.partner', string='Supplier')

    def check_stock_levels(self):
        products_to_replenish = self.env['product.product']
        for rule in self.env['product.reorder.rule'].search([]):
            if rule.product_id.qty_available < rule.minimum_stock:
                products_to_replenish += rule.product_id

        if products_to_replenish:
            self.generate_replenishment_orders(products_to_replenish)

    def generate_replenishment_orders(self, products):
        order_vals = []
        for product in products:
            rule = self.env['product.reorder.rule'].search([('product_id', '=', product.id)], limit=1)
            order_vals.append({
                'product_id': product.id,
                'product_qty': rule.reorder_quantity,
                'partner_id': rule.supplier_id.id,
                'picking_type_id': 1,  # Replace with the appropriate picking type ID
                'date_planned': fields.Datetime.now() + timedelta(days=rule.lead_time),
            })
        order = self.env['stock.picking'].create({
            'picking_type_id': 1,  # Replace with the appropriate picking type ID
            'partner_id': 1,  # Replace with the appropriate partner ID
            'move_lines': [(0, 0, line) for line in order_vals],
            'state': 'pending_approval',
        })
        order.action_approve_order()


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection(selection_add=[('pending_approval', 'Pending Approval')])

    def action_approve_order(self):
        self.write({'state': 'confirmed'})


