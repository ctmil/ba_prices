# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.osv import osv
from openerp.exceptions import except_orm, ValidationError
from StringIO import StringIO
import urllib2, httplib, urlparse, gzip, requests, json
import openerp.addons.decimal_precision as dp
import logging
from datetime import date
from openerp.fields import Date as newdate
from datetime import datetime,date

from openerp.addons.l10n_ar_fpoc.invoice import document_type_map, responsability_map

#Get the logger
_logger = logging.getLogger(__name__)

class product_product_price(models.Model):
	_inherit = 'product.product.price'
	
	def process_product_prices(self, cr, uid):
		
		product_ids = self.pool.get('product.product').search(cr,uid,[('sale_ok','=',True)])
		pricelist_ids = self.pool.get('product.pricelist').search(cr,uid,[('type','=','sale')])

		demo_partner = self.pool.get('res.partner').search(cr,uid,[('ref','=','CLIENTE_DEMO')])
		if not demo_partner:
			demo_partner = 1
		else:
			demo_partner = demo_partner[0]
		for product_id in product_ids:
			product = self.pool.get('product.product').browse(cr,uid,product_id)
			product_tmpl = product.product_tmpl_id
			for pl_id in pricelist_ids:
				price = self.pool.get('product.pricelist').price_get(cr,uid,[pl_id],product.id,1.0,1,{'uom':1})
				price = price[pl_id]
				vals = {
					'product_id': product_id,
					'pricelist_id': pl_id,
					'price': price,
					}
				ppp_id = self.pool.get('product.product.price').search(cr,uid,[('product_id','=',product_id),\
						('pricelist_id','=',pl_id)])
				if not ppp_id:
					return_id = self.pool.get('product.product.price').create(cr,uid,vals)
				else:
					return_id = self.pool.get('product.product.price').write(cr,uid,ppp_id,vals)
					
