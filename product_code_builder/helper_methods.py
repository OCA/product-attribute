# -*- coding: utf-8 -*-
# Copyright 2014- Odoo Community Association - OCA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import MissingError
import re
from string import Template
from collections import defaultdict

DEFAULT_REFERENCE_SEPARATOR = ''
PLACE_HOLDER_4_MISSING_VALUE = '/'


class ReferenceMask(Template):
    pattern = r'''\[(?:
                    (?P<escaped>\[) |
                    (?P<named>[^\]]+?)\] |
                    (?P<braced>[^\]]+?)\] |
                    (?P<invalid>)
                    )'''


def extract_token(s):
    pattern = re.compile(r'\[([^\]]+?)\]')
    return set(pattern.findall(s))


def sanitize_reference_mask(product, mask):
    tokens = extract_token(mask)
    attribute_names = set()
    for line in product.attribute_line_ids:
        attribute_names.add(line.attribute_id.name)
    if not tokens.issubset(attribute_names):
        raise MissingError(_('Found unrecognized attribute name in '
                             '"Partcode Template"'))


def get_rendered_default_code(product, mask):
    product_attrs = defaultdict(str)
    reference_mask = ReferenceMask(mask)
    for value in product.attribute_value_ids:
        if value.attribute_id.code:
            product_attrs[value.attribute_id.name] += value.attribute_id.code
        if value.code:
            product_attrs[value.attribute_id.name] += value.code
    all_attrs = extract_token(mask)
    missing_attrs = all_attrs - set(product_attrs.keys())
    missing = dict.fromkeys(missing_attrs, PLACE_HOLDER_4_MISSING_VALUE)
    product_attrs.update(missing)
    default_code = reference_mask.safe_substitute(product_attrs)
    return default_code


def render_default_code(product, mask):
    sanitize_reference_mask(product, mask)
    product.default_code = get_rendered_default_code(product, mask)
