from odoo import api, fields, models, _

class HospitalAppointment(models.Model):
    _name = 'test.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Appointment Management'

    name = fields.Char(string='Appointment Reference', copy=False, readonly=True, default='New')
    patient_id = fields.Many2one('test.patient', string='Patient', required=True)
    appointment_date = fields.Datetime(string='Appointment Date', required=True)
    doctor_id = fields.Many2one('res.users', string='Doctor', required=True)
    age = fields.Integer(related='patient_id.age', string='Patient Age', readonly=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], readonly=True)
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('test.appointment.sequence') or 'New'
        return super(HospitalAppointment, self).create(vals)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.onchange('patient_id')
    def _onchange_patient(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
        else:
            self.gender=''