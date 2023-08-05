import time

from zetsubou.utils import logger
from zetsubou.utils.error_codes import EErrorCode, ReturnErrorcode

def execute_stage(func, succ_msg: str, err_code: EErrorCode):
    start_time = time.time()
    result = func()
    end_time = time.time()

    if result is not None and result is not False:
        logger.Success(f'{succ_msg} - {end_time - start_time:.2f}sec')
        return result
    else:
        raise ReturnErrorcode(err_code)
