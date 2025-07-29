from odoo import api, fields, models, _


class HospitalPatient(models.Model):
    _name = 'test.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Management'

    name = fields.Char('Name', required=True)
    age = fields.Integer('Age', required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], required=True)
    medical_history = fields.Text('Medical History')
    note = fields.Text(string='Description', help='Description of the patient')
    message_follower_ids = fields.Many2many(
        'res.partner', 'patient_follower_rel', 'patient_id', 'partner_id',
        string='Followers', help='Partners following this patient')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('treated', 'Treated'),
        ('discharged', 'Discharged')
    ], string='Status', default='draft', tracking=True)
    parent_id = fields.Many2one(comodel_name='res.partner', string='Parent Patient', ondelete='cascade')
    sequence = fields.Char(string='Sequence', readonly=True, copy=False, default='New')
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count', store=True)


    def _compute_appointment_count(self):
        self.appointment_count = 2


    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('test.patient.sequence') or 'New'
        
        print("vals ------->", vals)
        record = super(HospitalPatient, self).create(vals)
        print("record ------->", record)
        return record
    

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'

    def action_treat(self):
        for record in self:
            record.state = 'treated'

    def action_reset(self):
        for record in self:
            record.state = 'draft'
