# -*- coding: utf-8 -*-

"""
Office Math Markup Language (OMML)
"""

import xml.etree.ElementTree as ET

from dwml.latex_dict import CHR,CHR_DEFAULT,POS,POS_DEFAULT,SUB,SUP,F

OMML_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"

def load(stream):
	tree = ET.parse(stream)
	for omath in tree.findall(OMML_NS+'oMath'):
		yield oMath2Latex(omath)


class oMath2Latex(object):
	"""

	"""

	def __init__(self,element):
		self._latex = self.process_children(element)
		

	def __str__(self):
		return self._latex

	def process_children(self,elm):
		latex_chars = list()
		getmetod = self.tag2meth.get
		for elm in list(elm):
			s_tag = elm.tag.replace(OMML_NS,'')
			meth = getmetod(s_tag)
			if meth :
				latex_chars.append(meth(self,elm))
		return ''.join(latex_chars)

	def get_latex(self):
		return self._latex

	def do_acc(self,elm):
		"""
		process the accent function
		"""
		chr_elm = elm.find('./{0}accPr/{0}chr'.format(OMML_NS))
		latex_func = None
		default_val  = CHR_DEFAULT.get('ACC_VAL')
		if chr_elm is None:
			latex_func = default_val
		else:
			char_val = chr_elm.get('{0}val'.format(OMML_NS))			
			latex_func = self.get_latex(char_val,store=CHR,default=default_val)
		text = self.do_e(elm.find('./{0}e'.format(OMML_NS)))
		return latex_func.format(text)

	def do_bar(self,elm):
		"""
		process the bar function
		"""
		pos_elm = elm.find('./{0}barPr/{0}pos'.format(OMML_NS))
		latex_func = None
		default_val  = POS_DEFAULT.get('POS_VAL')
		if pos_elm is None:
			latex_func = default_val
		else:
			char_val = pos_elm.get('{0}val'.format(OMML_NS))			
			latex_func = self.get_latex(char_val,store=POS,default=default_val)
		text = self.do_e(elm.find('./{0}e'.format(OMML_NS)))
		return latex_func.format(text)

	def do_box(self,elm):
		"""
		process the box object
		"""
		pass

	def do_d(self,elm):
		"""
		process the delimiter object
		"""
		pass

	def do_spre(self,elm):
		"""
		process the Pre-Sub-Superscript object -- Not support yet
		"""
		pass

	def do_ssub(self,elm):
		"""
		process the subscript object
		"""
		return self.process_children(elm)

	def do_ssup(self,elm):
		"""
		process the supscript object
		"""
		return self.process_children(elm)

	def do_ssubsup(self,elm):
		"""
		process the sub-superscript object
		"""
		return self.process_children(elm)

	def do_sub(self,elm):
		text = self.process_children(elm)
		return SUB.format(text)

	def do_sup(self,elm):
		text = self.process_children(elm)
		return SUP.format(text)

	def do_f(self,elm):
		"""
		process the fraction object
		"""
		num_elm = elm.find('./{0}num'.format(OMML_NS))
		num_text= self.do_num(num_elm)
		den_elm = elm.find('./{0}den'.format(OMML_NS))
		den_text= self.do_den(den_elm)
		return F.format(num=num_text,den=den_text)

	def do_num(self,elm):
		"""
		"""
		return self.process_children(elm)

	def do_den(self,elm):
		"""
		"""
		return self.process_children(elm)

	def do_e(self,elm):
		"""
		the "element object" has more unknown elements,so process all children of it
		"""
		return self.process_children(elm)

	def do_r(self,elm,format_str = '%s'):
		return format_str % elm.findtext('./{0}t'.format(OMML_NS))

	def get_latex(self,key,store=CHR,default=None):
		latex = store.get(key)
		return default if not latex else latex


	tag2meth={
		'acc' : do_acc,
		'e' : do_e,
		'r' : do_r,
		'bar' : do_bar,
		'sub' : do_sub,
		'sup' : do_sup,
		'sSub' : do_ssub,
		'sSup' : do_ssup,
		'sSubSup' : do_ssubsup,
		'f'   : do_f,
		'num' : do_num,
		'den' : do_den,
 	}





	




