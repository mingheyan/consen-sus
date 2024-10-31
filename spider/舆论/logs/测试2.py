from loggerr import logger
log = logger.bind(module_name='my-loguru')
log.debug("this is hello, module is my-loguru")

log2 = logger.bind(module_name='my-loguru2')
log2.info("this is hello, module is my-loguru2")
log.success('ss')