# -*- coding: utf-8 -*-
from odoo import models, fields

class KnowledgeTag(models.Model):
    _name = 'knowledge.tag'
    _description = 'Mot-clé (Tag) de la Base de Connaissances'
    _order = 'name'

    name = fields.Char(string="Nom du Tag", required=True)
    color = fields.Integer(string="Couleur") 