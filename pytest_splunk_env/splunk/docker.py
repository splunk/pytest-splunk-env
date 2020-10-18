import pytest
from .base import SplunkEnv
import logging
LOGGER = logging.getLogger(__name__)


class splunk_docker(SplunkEnv):
    this = "that"
