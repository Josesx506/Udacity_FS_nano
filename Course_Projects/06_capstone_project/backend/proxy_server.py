# Unsuccessful attempt to connect flask backend with node live-server frontend

# Use the ProxyFix middleware to handle the reverse proxy
# app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
# SITE_NAME = '127.0.0.1'
# Define proxy server.
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>', methods=['GET','POST','PUT','DELETE'])
# def proxy(path):
#   response = request.get_json(f'{SITE_NAME}{path}')
#   print(response)
#   return response