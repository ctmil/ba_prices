# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.osv import osv
from openerp.exceptions import except_orm, ValidationError
from StringIO import StringIO
import urllib2, httplib, urlparse, gzip, requests, json
import openerp.addons.decimal_precision as dp
import logging
import datetime
from openerp.fields import Date as newdate
from datetime import datetime,date

from openerp.addons.l10n_ar_fpoc.invoice import document_type_map, responsability_map

#Get the logger
_logger = logging.getLogger(__name__)

class product_product_price(models.Model):
	_name = 'product.product.price'
	_description = 'Tabla con los precios por diferente lista de precios'
	
	product_id = fields.Many2one('product.product')
	pricelist_id = fields.Many2one('product.pricelist')
	price = fields.Float('Precio')

