# -*- coding: utf-8 -*-
{
    'name': "Base de Connaissances (Wiki Interne)", 
    'version': '14.0.1.0.0',
    'summary': """
        Centralisez et partagez la connaissance de votre entreprise.
    """,
    'description': """
        Ce module fournit une application de type Wiki pour créer, organiser et 
        rechercher des articles et procédures internes.
    """,
    'author': "ATABONG EFON STEPHANE FRITZ", 
    'sequence': 1,
    'web_icon': 'knowledge_base/static/description/icon.png',
    'website': "https:atabong-portfolio.vercel.app", 
    'category': 'Knowledge Management',
    'depends': [
        'base',      
        'mail',      
        'hr',        
    ],
    'data': [      
        'security/ir.model.access.csv',

        'security/knowledge_base_security.xml',

        'views/knowledge_category_views.xml',
        'views/knowledge_tag_views.xml',
        'views/knowledge_article_rating_views.xml',

        'views/knowledge_article_views.xml',
        'views/knowledge_dashboard_views.xml',

        'views/knowledge_menus.xml',
    ],
    'installable': True,
    'application': True, 
    'auto_install': False,
    'license': 'LGPL-3',
}