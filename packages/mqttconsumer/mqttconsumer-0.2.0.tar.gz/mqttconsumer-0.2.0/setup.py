# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mqttconsumer']

package_data = \
{'': ['*']}

install_requires = \
['paho-mqtt>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'mqttconsumer',
    'version': '0.2.0',
    'description': 'Framework for MQTT-Consuming Analytics Applications',
    'long_description': 'This code facilitates the use of the MQTT protocol in analytics-related applications.\nIt is based on [Eclipse Paho™ MQTT Python Client](https://github.com/eclipse/paho.mqtt.python).\n',
    'author': 'Martin Trat',
    'author_email': 'martin.trat@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m-martin-j/mqttconsumer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
