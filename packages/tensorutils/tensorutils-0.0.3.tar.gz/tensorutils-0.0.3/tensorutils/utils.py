from logging import getLogger
from os import environ

logger = getLogger(__name__)


def select_cpu_if_not_gpu(incremental_memory: bool = False) -> None:
    """ Configure the suitable environment variables to use CPU when the GPU is not available for Tensorflow.
    :param incremental_memory: If True, configure the tensorflow to allow incremental memory allocation.
    """
    from tensorflow.config.experimental import list_physical_devices

    gpus = len(list_physical_devices('GPU'))
    if gpus:
        logger.info(f'Using {gpus} GPUs...')
        if incremental_memory:
            environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
    else:
        logger.warning('Not using CUDA GPU!')
        environ["CUDA_DEVICE_ORDER"] = 'PCI_BUS_ID'
        environ["CUDA_VISIBLE_DEVICES"] = ''
