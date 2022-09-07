import sys
from loguru import logger
from flask import request, Blueprint, Response


logger.remove()
logger.configure(
    extra={
        "service_name": "API",
        "context": {}
    }
)
log_format = '{level} {time} {extra[service_name]} {file} {function} "{message}" {extra[context]}'
logger.add(
    sys.stderr,
    format=log_format,
    catch=True,
    backtrace=True,
)

api = Blueprint('api', __name__, url_prefix=f'/api/v1')

@api.route('/health', methods=['GET'])
def healthcheck():
    log_context = {
        'ip':request.remote_addr,
        'method':request.method,
        'endpoint':'/health'
    }
    logger.bind(context=log_context).info('Обращение к проверке исправности')
    return Response(status=200)
