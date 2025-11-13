# see license/LICENSE.rst

from pathlib import Path

try:
    from ._version import version as __version__
    from ._version import version_tuple
except ImportError:
    __version__ = "unknown version"
    version_tuple = (0, 0, "unknown version")

package_directory = Path(__file__).parent
data_directory = package_directory / "data"
