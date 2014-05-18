# -*- encoding: utf-8 -*-
##############################################################################
#
#    Light-PosBox Software for Odoo
#    Copyright (C) 2014-TODAY Akretion <http://www.akretion.com>.
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#    @author Sébastien BEAU <sebastien.beau@akretion.com>
#
#    Some parts of the code come from Odoo project.
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

import json
import commands
import logging
import os

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import make_response
from flask import session
from uuid import uuid4
from flask.ext.babel import Babel
from flask.ext.babel import gettext as _

from cors_decorator import crossdomain
import escpos.driver
from escpos.driver import EscposDriver

# App Section
app = Flask(__name__)
app.config.from_pyfile('settings.py')
babel = Babel(app)

# Extra-Tools Section 
_logger = logging.getLogger(__name__)

# Drivers Section
drivers = {}
printerDriver = EscposDriver()
if app.config['PRINT_STATUS_START']:
    printerDriver.push_task('printstatus')
printerDriver.get_escpos_printer()
drivers['escpos'] = printerDriver

# Function Section
def get_status():
    statuses = {}
    for driver in drivers:
        statuses[driver] = drivers[driver].get_status()
    return statuses

# Generic Route Section
@app.route('/hw_proxy/hello', methods=['GET'])
@crossdomain(origin='*')
def hello():
    """ Simulate the behaviour of the function /hw_proxy/hello
    File Name: Odoo(V8) /addons/hw_proxy/controllers/main.py
    Function Name: Proxy::hello()
    """
    print "****** request /hw_proxy/hello/ ******"
    return make_response('ping')

@app.route('/hw_proxy/handshake', methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@crossdomain(origin='*', headers='accept, content-type')
def handshake():
    """ Simulate the behaviour of the function /hw_proxy/handshake
    File Name: Odoo(V8) /addons/hw_proxy/controllers/main.py
    Function Name: Proxy::handshake()
    """
    print "****** request /hw_proxy/handshake/ ******"
    return jsonify(jsonrpc='2.0', result = True)

@app.route('/hw_proxy/status', methods=['GET'])
@crossdomain(origin='*')
def status_http():
    """ Simulate the behaviour of the function /hw_proxy/status
    File Name: Odoo(V8) /addons/hw_proxy/controllers/main.py
    Function Name: Proxy::status_http()
    """
    statuses = {}
    for driver in drivers:
        import flask
        statuses[driver] = {
            'state': drivers[driver].get_status(),
            'image': 'static/' + drivers[driver].get_image_name(),
        }
    devices = commands.getoutput("lsusb").split('\n')
    return render_template(
        'status.html', statuses=statuses, devices=devices)

@app.route('/hw_proxy/static/escpos/images/<path:path>', methods=['POST', 'GET', 'PUT', 'OPTIONS'])
def get_image(path=None):
    print "coincoin"
    
    return app.send_static_file(os.path.join('escpos/images/', path))

@app.route('/hw_proxy/status_json', methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@crossdomain(origin='*', headers='accept, content-type')
def status_json():
    """ Simulate the behaviour of the function /hw_proxy/status_json
    File Name: Odoo(V8) /addons/hw_proxy/controllers/main.py
    Function Name: Proxy::status_json()
    """
    print "****** request /hw_proxy/status_json/ ******"
    statuses = {}
    for driver in drivers:
        statuses[driver] = drivers[driver].get_status()
    return jsonify(jsonrpc='2.0', result = statuses)


# EscPos Route Section
@app.route('/hw_proxy/open_cashbox', methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@crossdomain(origin='*', headers='accept, content-type')
def open_cashbox():
    _logger.info('ESC/POS: OPEN CASHBOX')
    drivers['escpos'].push_task('cashbox')

@app.route('/hw_proxy/print_receipt', methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@crossdomain(origin='*', headers='accept, content-type')
def print_receipt():
    _logger.info('ESC/POS: PRINT RECEIPT')
    receipt = request.json['params']['receipt']
    drivers['escpos'].push_task('receipt',receipt)


@app.route('/hw_proxy/print_xml_receipt', methods=['POST', 'GET', 'PUT', 'OPTIONS'])
@crossdomain(origin='*', headers='accept, content-type')
def print_xml_receipt():
    _logger.info('ESC/POS: PRINT XML RECEIPT')
    receipt = request.json['params']['receipt']
    drivers['escpos'].push_task('xml_receipt',receipt)


### Run application
if __name__ == '__main__':
    app.run(debug=True)
#    app.run()


#class EscposProxy(hw_proxy.Proxy):

#    @http.route('/hw_proxy/escpos/add_supported_device', type='http', auth='none', cors='*')
#    def add_supported_device(self, device_string):
#        _logger.info('ESC/POS: ADDED NEW DEVICE:'+device_string) 
#        driver.add_supported_device(device_string)
#        return "The device:\n"+device_string+"\n has been added to the list of supported devices.<br/><a href='/hw_proxy/status'>Ok</a>"

#    @http.route('/hw_proxy/escpos/reset_supported_devices', type='http', auth='none', cors='*')
#    def reset_supported_devices(self):
#        try:
#            os.remove('escpos_devices.pickle')
#        except Exception as e:
#            pass
#        return 'The list of supported devices has been reset to factory defaults.<br/><a href="/hw_proxy/status">Ok</a>'
