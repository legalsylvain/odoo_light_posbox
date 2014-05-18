# -*- encoding: utf-8 -*-
##############################################################################
#
#    hw_escpos Module for Odoo
#    Copyright (C) Odoo SA.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""This is a list of esc/pos compatible usb printers. The vendor and product
ids can be found by typing lsusb in a linux terminal, this will give you the
ids in the form ID VENDOR:PRODUCT
"""
device_list = [
    {'vendor': 0x04b8, 'product': 0x0e03, 'name': 'Epson TM-T20'},
    {'vendor': 0x04b8, 'product': 0x0202, 'name': 'Epson TM-T70'},
]
