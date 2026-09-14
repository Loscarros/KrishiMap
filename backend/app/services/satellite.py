
from typing import Any


# =========================================================
# FREE SATELLITE SERVICE
# =========================================================
#
# This project does NOT use Sentinel Hub.
#
# No:
#   - Sentinel Hub account
#   - OAuth credentials
#   - Client ID
#   - Client secret
#   - Paid satellite API
#
# The recommendation engine is designed to work even
# when satellite observations are unavailable.
#
# A free/public satellite provider can be connected later
# without changing the recommendation API contract.
# =========================================================


def get_empty_satellite_result() -> dict[str, Any]:
    """
    Standard response when satellite observations
    are unavailable.
    """

    return {
        "available": False,

        "source": None,

        "acquisition_window_days": None,

        "ndvi": None,

        "ndmi": None,

        "bsi": None,

        "cloud_masked": False,
    }


# =========================================================
# CONFIGURATION
# =========================================================

def satellite_is_configured() -> bool:
    """
    Satellite integration is intentionally disabled.

    This keeps the current project completely free and
    avoids requiring any commercial satellite API account.
    """

    return False


# =========================================================
# MAIN FUNCTION
# =========================================================

async def get_satellite_indicators(
    boundary: dict,
) -> dict[str, Any]:
    """
    Return satellite indicators for a farm.

    Current implementation:

        No external satellite API.

    Therefore:

        available = False

        ndvi = None
        ndmi = None
        bsi = None

    The rest of the application continues normally.
    """

    # -----------------------------------------------------
    # Validate the GeoJSON boundary.
    # -----------------------------------------------------

    if (
        not boundary
        or boundary.get("type") != "Polygon"
    ):
        return get_empty_satellite_result()


    # -----------------------------------------------------
    # Satellite integration is currently disabled.
    # -----------------------------------------------------

    return get_empty_satellite_result()