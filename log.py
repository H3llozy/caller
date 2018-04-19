import logging

__logger = logging.getLogger(__name__)
__logger.setLevel(logging.DEBUG)

# try:
#     import coloredlogs
#
#     coloredlogs.install(level='DEBUG', logger=__logger,
#                         fmt='[%(asctime)s %(filename)s %(lineno)d'
#                         ' %(levelname)s] %(message)s')
# except ModuleNotFoundError:
#     fmt = logging.Formatter('[%(asctime)s %(filename)s %(lineno)d'
#                             ' %(levelname)s] %(message)s')
#
#     handler = logging.StreamHandler()
#     handler.setLevel(logging.DEBUG)
#     handler.setFormatter(fmt)
#
#     __logger.addHandler(handler)
#     __logger.setLevel(logging.DEBUG)


debug = __logger.debug
info = __logger.info
warning = __logger.warning

if __name__ == '__main__':
    debug("%s %s", "2", "3")
