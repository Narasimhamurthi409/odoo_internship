from odoo import models, fields

class CarRental(models.Model):
    _name = "car.rental"
    _description = "Car Rental"
    _inherit = ['mail.thread']  # Optional: Adds chatter/tracking

    car_name = fields.Char(string="Car Name", required=True, tracking=True)  # Track changes
    car_model = fields.Char(string="Car Model", required=True)
    wheel_type = fields.Selection([
        ('alloy', 'Alloy'),
        ('steel', 'Steel'),
        ('carbon_fiber', 'Carbon Fiber')
    ], string="Wheel Type", required=True)
    body_color = fields.Char(string="Body Color", required=True)
    available = fields.Boolean(string="Available", default=True)
    seat_count = fields.Integer(string="Seat Count", required=True, default=4)
    amount = fields.Float(string="Amount", required=True)