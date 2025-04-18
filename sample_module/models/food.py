from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Food(models.Model):
    _name = "food.food"
    _description = "Food Management System"
    _rec_name = "partner_id"

    # Fields
    partner_id = fields.Many2one(
        'res.partner', 
        string="Customer", 
        required=True
    )
    price = fields.Float(string="Price")
    quantity = fields.Integer(string="Quantity")
    review = fields.Text(string="Review")
    is_satisfied = fields.Boolean(string="Satisfied?")
    check_in = fields.Date(string="Check-In Date")
    served_time = fields.Datetime(string="Served Time")
    types = fields.Selection(
        [('dine_in', 'Dine-In'), 
         ('delivery', 'Delivery')], 
        string="Service Type"
    )
    images = fields.Binary(string="Food Image")
    blog = fields.Html(string="Blog Content")
    sale_order_id = fields.Many2one(
        'sale.order', 
        string="Sale Order", 
        readonly=True
    )
    invoice_id = fields.Many2one(
        'account.move', 
        string="Invoice", 
        readonly=True
    )
    sale_created = fields.Boolean(
        string="Sale Created", 
        invisible=True
    )
    date_of_birth = fields.Date(string="Customer DOB")
    age = fields.Integer(
        string="Age", 
        compute="_compute_age", 
        store=True
    )

    # Methods
    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = date.today()
                born = record.date_of_birth
                record.age = today.year - born.year - (
                    (today.month, today.day) < (born.month, born.day))
            else:
                record.age = 0

    def create_sale_order(self):
        """Create sale order from food record"""
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'order_line': [(0, 0, {
                'product_id': self._get_default_product().id,
                'product_uom_qty': self.quantity,
                'price_unit': self.price
            })]
        })
        self.write({
            'sale_order_id': sale_order.id,
            'sale_created': True
        })
        return sale_order

    def _get_default_product(self):
        """Get default product for sale orders"""
        return self.env.ref('product.product_product_4')  # Change to your actual product XML ID

    def purchase_records(self):
        """Find food records meeting criteria"""
        return self.search([
            ('price', '>', 100),
            ('is_satisfied', '=', True)
        ])

    def change_the_record(self):
        """Update record values"""
        return self.write({
            'review': "Updated via button click",
            'quantity': 1000
        })

    def delet_the_rec(self):
        """Delete current record"""
        return self.unlink()

    @api.model
    def default_get(self, fields_list):
        """Set default values when creating new records"""
        defaults = super().default_get(fields_list)
        defaults.update({
            'review': "Default review text",
            'is_satisfied': True
        })
        return defaults

    @api.constrains('price')
    def _check_price(self):
        """Ensure price is positive"""
        for record in self:
            if record.price < 0:
                raise ValidationError("Price cannot be negative!")