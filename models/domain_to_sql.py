from odoo import models, fields

def get_query(self, args, operation, field, start_date=None, end_date=None,
              group_by=False, apply_ir_rules=False):
    
    query = self._where_calc(args)
    if apply_ir_rules:
        self._apply_ir_rules(query, 'read')
    if operation and field:
        data = 'COALESCE(%s("%s".%s),0) AS value' % (
            operation.upper(), self._table, field.name)
        join = ''
        group_by_str = ''
        if group_by and group_by.name == 'product_id':
            model_name = self._name
            field_relation = self.env[model_name]._fields.get('product_id')
            if isinstance(field_relation,
                          fields.Many2one) and field_relation.comodel_name == 'product.product':
                join += """
                           INNER JOIN product_product ON product_product.id = "%s".product_id
                           INNER JOIN product_template ON product_template.id = product_product.product_tmpl_id
                       """ % self._table
                data += ', product_template.name AS product_name'
                group_by_str = ' GROUP BY product_template.name'

        elif group_by and group_by.name == 'categ_id':
            model_name = self._name
            field_relation = self.env[model_name]._fields.get('product_id')
            if isinstance(field_relation,
                          fields.Many2one) and field_relation.comodel_name == 'product.product':
                join += """
                           INNER JOIN product_product ON product_product.id = "%s".product_id
                           INNER JOIN product_template ON product_template.id = product_product.product_tmpl_id
                           INNER JOIN product_category ON product_category.id = product_template.categ_id
                       """ % self._table
                data += ', product_category.complete_name AS categ_name'
                group_by_str = ' GROUP BY product_category.complete_name'

        elif group_by:
            if group_by.ttype == 'many2one':
                relation_model = group_by.relation.replace('.', '_')
                join = ' INNER JOIN %s on "%s".id = "%s".%s' % (
                    relation_model, relation_model, self._table, group_by.name)
                rec_name = self.env[group_by.relation]._rec_name_fallback()
                data = data + ',"%s".%s AS %s' % (
                    relation_model, rec_name, group_by.name)
                group_by_str = ' Group by "%s".%s' % (relation_model, rec_name)
            else:
                data = data + ',"%s".%s' % (self._table, group_by.name)
                group_by_str = ' Group by "%s".%s' % (
                    self._table, str(group_by.name))
                
    else:
        data = '"%s".id' % (self._table)

    from_clause, from_params = query.from_clause
    where_clause, where_clause_params = query.where_clause
    where_str = where_clause and (" WHERE %s" % where_clause) or ''

    if start_date and start_date != 'null':
        start_date_query = f' AND ({from_clause}."create_date" >= \'{start_date}\')'
    else:
        start_date_query = ''
    
    if end_date and end_date != 'null':
        end_date_query = f' AND ({from_clause}."create_date" <= \'{end_date}\')'
    else:
        end_date_query = ''

    query_str = 'SELECT %s FROM ' % data + from_clause + join + where_str + start_date_query + end_date_query + group_by_str

    def format_param(x):
        if not isinstance(x, tuple):
            return "'" + str(x) + "'"
        elif isinstance(x, tuple) and len(x) == 1:
            return "(" + str(x[0]) + ")"
        else:
            return str(x)
        

    exact_query = query_str % tuple(map(format_param, where_clause_params))
    return exact_query

models.BaseModel.get_query = get_query