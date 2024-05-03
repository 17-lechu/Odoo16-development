{
    'name': 'Inventory Customisation',
    'version': '1.6',
    'category': 'Inventory',
    "sequence": 1,
    'summary': 'Inventory Management',
    'complexity': 'User Friendly',
    'description': """
            This module provides that automatically generate the replenishment orders based on lead time and the
             supplier.
    """,
    'author': 'Lekshmi G S',
    'website': '',
    'depends': ['base', 'stock', 'purchase'],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/product_reorder_rule.xml',
        'menu/menu.xml'
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
