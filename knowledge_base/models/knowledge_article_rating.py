# -*- coding: utf-8 -*-
from odoo import models, fields, api

class KnowledgeArticleRating(models.Model):
    _name = 'knowledge.article.rating'
    _description = 'Note d\'un Article de la Base de Connaissances'
    _order = 'create_date desc'

    article_id = fields.Many2one(
        'knowledge.article', 
        string="Article", 
        required=True, 
        ondelete='cascade'
    )
    user_id = fields.Many2one(
        'res.users', 
        string="Utilisateur", 
        required=True, 
        default=lambda self: self.env.user
    )
    rating = fields.Selection([
        ('1', '⭐'),
        ('2', '⭐⭐'),
        ('3', '⭐⭐⭐'),
        ('4', '⭐⭐⭐⭐'),
        ('5', '⭐⭐⭐⭐⭐')
    ], string="Note", required=True)
    feedback = fields.Text(string="Commentaire (Optionnel)")

    # Contrainte pour s'assurer qu'un utilisateur ne note qu'une seule fois un article
    _sql_constraints = [
        ('unique_article_user_rating', 'unique(article_id, user_id)', 
         'Vous avez déjà noté cet article !')
    ]