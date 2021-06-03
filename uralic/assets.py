from pathlib import Path

from clld.web.assets import environment

import uralic


environment.append_path(
    Path(uralic.__file__).parent.joinpath('static').as_posix(),
    url='/uralic:static/')
environment.load_path = list(reversed(environment.load_path))
