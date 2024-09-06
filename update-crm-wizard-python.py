# File: wizards/update_crm_wizard.py

from odoo import api, fields, models

class UpdateCRMWizard(models.TransientModel):
    _name = 'update.crm.wizard'
    _description = 'Update CRM Wizard'

    team_id = fields.Many2one('crm.team', string='Sales Team', required=True)
    user_id = fields.Many2one('res.users', string='Salesperson', domain="[('id', 'in', available_user_ids)]")
    available_user_ids = fields.Many2many('res.users', compute='_compute_available_users')

    @api.depends('team_id')
    def _compute_available_users(self):
        for wizard in self:
            wizard.available_user_ids = wizard.team_id.member_ids

    def action_update_crm(self):
        active_ids = self.env.context.get('active_ids', [])
        leads = self.env['crm.lead'].browse(active_ids)
        leads.write({
            'team_id': self.team_id.id,
            'user_id': self.user_id.id,
        })
        return {'type': 'ir.actions.act_window_close'}
