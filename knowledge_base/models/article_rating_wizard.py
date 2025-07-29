# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ArticleRatingWizard(models.TransientModel):
    _name = 'knowledge.article.rating.wizard'
    _description = 'Assistant de Notation d\'Article'

    # Le champ que l'utilisateur va remplir
    rating = fields.Selection([
        ('1', '⭐ Très mauvais'),
        ('2', '⭐⭐ Mauvais'),
        ('3', '⭐⭐⭐ Moyen'),
        ('4', '⭐⭐⭐⭐ Bon'),
        ('5', '⭐⭐⭐⭐⭐ Excellent')
    ], string="Votre Note", required=True, default='4') # default à 4 pour encourager
    
    feedback = fields.Text(string="Votre commentaire (optionnel)")
    
    # Un champ pour garder en mémoire l'article que l'on est en train de noter
    article_id = fields.Many2one('knowledge.article', string="Article", readonly=True)

    def action_submit_rating(self):
        """
        Cette méthode est appelée quand l'utilisateur clique sur "Soumettre".
        """
        self.ensure_one() # S'assure qu'on travaille sur un seul wizard à la fois

        # On vérifie si l'utilisateur n'a pas déjà noté
        existing_rating = self.env['knowledge.article.rating'].search([
            ('article_id', '=', self.article_id.id),
            ('user_id', '=', self.env.user.id)
        ], limit=1)

        if existing_rating:
            # Si une note existe déjà, on la met simplement à jour
            existing_rating.write({
                'rating': self.rating,
                'feedback': self.feedback
            })
        else:
            # Sinon, on crée une nouvelle note
            self.env['knowledge.article.rating'].create({
                'article_id': self.article_id.id,
                'user_id': self.env.user.id,
                'rating': self.rating,
                'feedback': self.feedback,
            })
        
        # On retourne une action pour fermer le wizard
        return {'type': 'ir.actions.act_window_close'}