{
    'name': 'Price tracking',
    'version': '1.0.0',
    'category': 'Tools',
    'summary': 'Reporte de cambios de precios',
    'author': 'Oscar Rugama',
    'website': 'https://www.ak.com.ni',
    'depends': ['base','stock', 'product','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/price_tracking.xml',
    ],
    'installable': True,
    'application': False,
}
#