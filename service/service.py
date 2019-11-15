from flask import Flask, request, Response
import os
import requests
import logging
import cherrypy
import paste.translogger
import json
from sesamutils import Dotdictify

app = Flask(__name__)
format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger('ELMA-Service')

with open("banner.txt", 'r') as banner:
    for line in banner:
        cherrypy.log(repr(line))
    cherrypy.log("")

# Log to stdout
# stdout_handler = logging.StreamHandler()
# stdout_handler.setFormatter(logging.Formatter(format_string))
# logger.addHandler(stdout_handler)
# logger.setLevel(logging.DEBUG)
page = 1


def stream_as_json(generator_function):
    first = True
    yield '['
    for item in generator_function:
        if not first:
            yield ','
        else:
            first = False
        yield json.dumps(item)
    yield ']'

def get_entries(page=page):
    try:
        base_url = "http://hotell.difi.no/api/json/difi/elma/participants"
        nestedpath = "entries" #request.args.get("nestedpath")
        logger.info(f"Fetching data from url: {base_url}")
        logger.info(f"fetching data from page: {page}.")
        count = 0

        while True:
            param = f'?page={page}'
            req = requests.get(base_url + param)
            req.encoding = 'utf-8'
            page = int(page)

            if req.ok:
                data = json.loads(req.text)
                lastpage = data['pages']
                if page > lastpage:
                    break
                try:
                    page += 1
                except:
                    logger.info("page + 1 did not work" + str(type(page)))

                for item in data[f'{nestedpath}']:
                    i = dict(item)
                    try:
                        i["_id"] = item[f'identifier']+"-"+item['Icd']
                        i["_updated"] = page
                    except Exception as e:
                        logger.error(f"ERROR: {e}")
                    yield i
                    count +=1
                    

            else:
                raise ValueError(f'value object expected in response to url: {base_url} got {req}')
                break
        
        logger.info(f'Yielded: {count}, last page: {page}. Since set to {(page -1)}')
    except Exception as e:
        logger.error(f"def get_entities issue: {e}")

        
@app.route("/entries")
def entities():
    try:
        if request.args.get('since') is None:
            page = 1
            logger.info("since value is set to page " + str(page))
        else:
            pagestr = request.args.get('since')
            page = int(pagestr) -1
            logger.info("since/page set to " + str(page))
        return Response(stream_as_json(get_entries(page)), mimetype='application/json')
    except Exception as e:
        logger.error(f"def entities issue: {e}")


if __name__ == '__main__':
    format_string = '%(name)s - %(levelname)s - %(message)s'
    # Log to stdout, change to or add a (Rotating)FileHandler to log to a file
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(logging.Formatter(format_string))
    logger.addHandler(stdout_handler)

    # Comment these two lines if you don't want access request logging
    app.wsgi_app = paste.translogger.TransLogger(app.wsgi_app, logger_name=logger.name,
                                                 setup_console_handler=False)
    app.logger.addHandler(stdout_handler)

    logger.propagate = False
    log_level = logging.getLevelName(os.environ.get('LOG_LEVEL', 'INFO'))  # default log level = INFO
    logger.setLevel(level=log_level)
    cherrypy.tree.graft(app, '/')
    # Set the configuration of the web server to production mode
    cherrypy.config.update({
        'environment': 'production',
        'engine.autoreload_on': False,
        'log.screen': True,
        'server.socket_port': 5000,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()