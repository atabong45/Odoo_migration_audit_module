# -*- coding: utf-8 -*-
from odoo import models, fields, api

class KnowledgeCategory(models.Model):
    _name = 'knowledge.category'
    _description = 'Catégorie de la Base de Connaissances'
    _order = 'name'

    name = fields.Char(string="Nom de la Catégorie", required=True)
    description = fields.Text(string="Description")
    
    # --- Champs pour la hiérarchie ---
    parent_id = fields.Many2one(
        'knowledge.category', 
        string="Catégorie Parente", 
        ondelete='cascade', 
        index=True
    )
    child_ids = fields.One2many(
        'knowledge.category', 
        'parent_id', 
        string="Sous-catégories"
    )

    # --- Champ calculé pour le nombre d'articles ---
    article_count = fields.Integer(
        string="Nombre d'Articles", 
        compute='_compute_article_count'
    )

    def _compute_article_count(self):
        for category in self:
            count = self.env['knowledge.article'].search_count([
                ('category_id', 'child_of', category.id)
            ])
            category.article_count = count