#!/usr/bin/python
import sys, os

os.chdir("/home/park0odf/www.testparkingsector.bg")
os.environ['DJANGO_SETTINGS_MODULE'] = "Version1.settings"
base = os.path.dirname(os.path.abspath(__file__)) + '/..'
sys.path.append(base)

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded",daemonize="false")
#runfastcgi(method="threaded",daemonize="false", maxrequests=100)
#runfastcgi(protocol="fcgi", socket="/tmp/aaa.sock", method="prefork", daemonize="false" , errlog="/tmp/log.err")

#WSGIServer: missing FastCGI param REQUEST_METHOD required by WSGI!
#WSGIServer: missing FastCGI param SERVER_NAME required by WSGI!
#WSGIServer: missing FastCGI param SERVER_PORT required by WSGI!
#WSGIServer: missing FastCGI param SERVER_PROTOCOL required by WSGI!


