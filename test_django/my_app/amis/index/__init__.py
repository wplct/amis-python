from amis_python import register_page

register_page("页面","/index")

from .index import *
from .error import *
from .form import *