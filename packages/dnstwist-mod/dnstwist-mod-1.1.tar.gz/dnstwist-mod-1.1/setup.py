from setuptools import setup

def get_extras(rel_path):
	with open(rel_path) as f:
		extras = [line for line in f.read().splitlines() if not line.startswith('#')]
	return extras

def get_version(rel_path):
	with open(rel_path) as f:
		for line in f.read().splitlines():
			if line.startswith('__version__'):
				delim = '"' if '"' in line else "'"
				return line.split(delim)[1]
	raise RuntimeError('Unable to find version string')

setup(
	name='dnstwist-mod',
	version='1.1',
	author='Marcin Ulikowski',
	author_email='marcin@ulikowski.pl',
	description='Domain name permutation engine for detecting homograph phishing attacks, typo squatting, and brand impersonation',
	long_description='Project website: https://github.com/elceef/dnstwist',
	url='https://github.com/elceef/dnstwist',
	license='ASL 2.0',
	py_modules=['dnstwist'],
	entry_points={
		'console_scripts': ['dnstwist=dnstwist:run']
	},
	install_requires=[],
	extras_require={
		'full': ['#GeoIP>=1.3.2', 'geoip2>=4.0.0', 'dnspython>=1.16.0', '#ssdeep>=3.1', 'ppdeep>=20200505', 'whois>=0.8', 'tld>=0.9.1', 'idna>=2.8'],
	},
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: Apache Software License',
		'Operating System :: OS Independent',
	],
)
