# -*- coding: utf-8 -*-
from odoo import models, fields, api

class KnowledgeArticle(models.Model):
    _name = 'knowledge.article'
    _inherit = ['mail.thread', 'mail.activity.mixin'] 
    _description = 'Article de la Base de Connaissances'
    _order = 'name'

    name = fields.Char(string="Titre", required=True, tracking=True)
    active = fields.Boolean(string="Actif", default=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('published', 'Publié')
    ], string="État", default='draft', required=True, tracking=True)
    
    content = fields.Html(string="Contenu")
    
    # --- Relations ---
    category_id = fields.Many2one(
        'knowledge.category', 
        string="Catégorie", 
        required=True, 
        ondelete='restrict'
    )
    tag_ids = fields.Many2many(
        'knowledge.tag', 
        string="Mots-clés"
    )
    author_id = fields.Many2one(
        'res.users', 
        string="Auteur", 
        readonly=True, 
        default=lambda self: self.env.user
    )
    
    # --- Rating ---
    rating_ids = fields.One2many(
        'knowledge.article.rating', 
        'article_id', 
        string="Notes"
    )
    average_rating = fields.Float(
        string="Note Moyenne", 
        compute='_compute_average_rating', 
        store=True, 
        digits=(3, 2),
        default=0.0  # Valeur par défaut pour éviter les erreurs
    )
    rating_count = fields.Integer(
        string="Nombre de notes",
        compute='_compute_rating_count',
        store=True,  # Stocker pour éviter les recalculs
        default=0
    )
    
    view_count = fields.Integer(string="Nombre de Vues", default=0, readonly=True)
    color = fields.Integer(string='Index Couleur', default=0)

    @api.depends('rating_ids')
    def _compute_rating_count(self):
        for article in self:
            article.rating_count = len(article.rating_ids) if article.rating_ids else 0

    @api.depends('rating_ids.rating')
    def _compute_average_rating(self):
        for article in self:
            if article.rating_ids:
                try:
                    # On convertit les notes en entiers pour le calcul
                    ratings = [int(r.rating) for r in article.rating_ids if r.rating]
                    if ratings:
                        article.average_rating = sum(ratings) / len(ratings)
                    else:
                        article.average_rating = 0.0
                except (ValueError, TypeError):
                    # En cas d'erreur de conversion, on met 0
                    article.average_rating = 0.0
            else:
                article.average_rating = 0.0

    # Méthodes pour les boutons 
    def action_publish(self):
        self.write({'state': 'published'})

    def action_set_to_draft(self):
        self.write({'state': 'draft'})

    def action_open_rating_wizard(self):
        """
        Ouvre l'assistant de notation pour l'article courant.
        """
        self.ensure_one()
        # Vérifier si l'utilisateur a déjà noté cet article
        existing_rating = self.env['knowledge.article.rating'].search([
            ('article_id', '=', self.id),
            ('user_id', '=', self.env.user.id)
        ], limit=1)
        
        if existing_rating:
            # Si l'utilisateur a déjà noté, on peut soit empêcher la re-notation
            # soit permettre la modification de sa note existante
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Information',
                    'message': 'Vous avez déjà noté cet article.',
                    'type': 'warning',
                }
            }
        
        # Crée un wizard pré-rempli avec l'ID de l'article courant
        wizard = self.env['knowledge.article.rating.wizard'].create({
            'article_id': self.id,
        })
        
        # Retourne une action qui ouvre la vue du wizard en mode formulaire
        return {
            'name': 'Noter cet article',
            'type': 'ir.actions.act_window',
            'res_model': 'knowledge.article.rating.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new', # 'new' signifie que ça s'ouvre en pop-up
        }
    
    def read(self, fields=None, load='_classic_read'):
        """ Surcharge la méthode read pour incrémenter le compteur de vues. """
        # On appelle d'abord la méthode parente pour obtenir le comportement normal
        result = super(KnowledgeArticle, self).read(fields=fields, load=load)
        
        # On incrémente le compteur uniquement si on lit un seul enregistrement (typiquement, en ouvrant la vue formulaire)
        # et pour éviter de le faire sur des opérations de recherche en arrière-plan.
        if len(self) == 1 and not self.env.context.get('skip_view_count'):
            try:
                # On utilise une requête SQL directe pour la performance et pour éviter des boucles de récursion.
                # Cela met à jour le compteur sans déclencher d'autres écritures ou calculs.
                self.env.cr.execute('UPDATE knowledge_article SET view_count = view_count + 1 WHERE id = %s', [self.id])
                # Ne pas faire de commit ici, laisser Odoo gérer les transactions
            except Exception:
                # En cas d'erreur, on ignore silencieusement
                pass
            
        return result