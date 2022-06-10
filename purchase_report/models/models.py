# -*- coding: utf-8 -*-

from odoo import models


class InvoiceInheritReport(models.AbstractModel):
    _name = 'report.purchase_report.purchase_report_id'
    _description = 'Product Quantity Color and size wise'

    def _get_report_values(self, docids, data=None):
        purchase_order = self.env['purchase.order'].browse((docids[0]))
        for rec in purchase_order:
            product_data = []
            for i in rec.order_line:
                try:
                    if i.product_id.sh_is_bundle:
                        # get product_name , color, size_range, Assortment
                        color_name = self.get_color_name(i.product_id)
                        size_range, assortment = self.get_assortment_size_range(i.product_id)
                        product_combine_name = i.product_id.name
                        split_res = product_combine_name.split('-')
                        product_name = ''
                        product_color = ''
                        for rec in split_res:
                            if color_name.upper() == rec.upper():
                                product_color = rec
                                break
                            else:
                                product_name += rec

                        dict_exist = next(
                            (item for item in product_data if item['product_id'] ==
                             i.product_id.id), None)
                        if not dict_exist:
                            new_dict = {
                                'product_id': i.product_id.id,
                                'product_name': product_name,
                                'color': product_color,
                                'size_range': size_range,
                                'assortment': assortment,
                                'line_total_qty': i.product_qty,
                                'retail_price': i.price_unit,
                                'sizes': [{
                                    '39': 0,
                                    '40': 0,
                                    '41': 0,
                                    '42': 0,
                                    '43': 0,
                                    '44': 0,
                                    '45': 0,
                                    '46': 0,
                                }]
                            }
                            for line in i.product_id.product_tmpl_id.sh_bundle_product_ids:
                                product_attribute = line.sh_product_id.product_template_attribute_value_ids
                                size = product_attribute.filtered(
                                    lambda attribute: attribute.attribute_id.name.upper() == 'SIZE'
                                )
                                new_dict['sizes'][0][size.name] += i.product_qty * line.sh_qty
                            product_data.append(new_dict)
                        else:
                            for line in i.product_id.product_tmpl_id.sh_bundle_product_ids:
                                product_attribute = line.sh_product_id.product_template_attribute_value_ids
                                size = product_attribute.filtered(
                                    lambda attribute: attribute.attribute_id.name.upper() == 'SIZE'
                                )
                                dict_exist['sizes'][0][size.name] += i.product_qty * line.sh_qty
                    else:
                        self.create_line_without_qty(product_data, i)
                except Exception as e:
                    self.create_line_without_qty(product_data, i)
        return {
            'doc_model': purchase_order,
            'data': data,
            'product_data': product_data,
        }

    def get_color_name(self, product):
        for rec in product:
            if rec.sh_bundle_product_ids:
                for line in rec.sh_bundle_product_ids:
                    product_attribute = line.sh_product_id.product_template_attribute_value_ids
                    color_id = product_attribute.filtered(
                        lambda attribute: attribute.attribute_id.name.upper() == 'COLOR'
                    )
                    return color_id.name

    def get_assortment_size_range(self, product=None):
        size_range = []
        assortment = []
        for rec in product:
            if rec.sh_bundle_product_ids:
                for assort in rec.sh_bundle_product_ids:
                    assortment.append(int(assort.sh_qty))
                for size in rec.sh_bundle_product_ids:
                    product_attribute = size.sh_product_id.product_template_attribute_value_ids
                    size = product_attribute.filtered(
                        lambda attribute: attribute.attribute_id.name.upper() == 'SIZE'
                    )
                    size_range.append(size.name)
        assortment = '-'.join([str(assortment[i]) for i in range(len(assortment))])
        size_range = size_range[0] + '-' + size_range[-1]
        return '(' + size_range + ')', '(' + assortment + ')'

    def create_line_without_qty(self, variant_values=None, i=None):
        variant_values.append({
            'product_id': i.product_id.id,
            'product_name': i.product_id.name,
            'color': '-',
            'size_range': '-',
            'assortment': '-',
            'retail_price': i.price_unit,
            'line_total_qty': i.product_qty,
            'sizes': [{
                '39': 0,
                '40': 0,
                '41': 0,
                '42': 0,
                '43': 0,
                '44': 0,
                '45': 0,
                '46': 0,
            }]
        })
        return variant_values
