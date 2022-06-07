# -*- coding: utf-8 -*-
# from odoo import http


# class InvoicePairPrice(http.Controller):
#     @http.route('/invoice_pair_price/invoice_pair_price/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_pair_price/invoice_pair_price/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_pair_price.listing', {
#             'root': '/invoice_pair_price/invoice_pair_price',
#             'objects': http.request.env['invoice_pair_price.invoice_pair_price'].search([]),
#         })

#     @http.route('/invoice_pair_price/invoice_pair_price/objects/<model("invoice_pair_price.invoice_pair_price"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_pair_price.object', {
#             'object': obj
#         })
