
# from typing import Any


# # =========================================================
# # FREE SATELLITE SERVICE
# # =========================================================
# #
# # This project does NOT use Sentinel Hub.
# #
# # No:
# #   - Sentinel Hub account
# #   - OAuth credentials
# #   - Client ID
# #   - Client secret
# #   - Paid satellite API
# #
# # The recommendation engine is designed to work even
# # when satellite observations are unavailable.
# #
# # A free/public satellite provider can be connected later
# # without changing the recommendation API contract.
# # =========================================================


# def get_empty_satellite_result() -> dict[str, Any]:
#     """
#     Standard response when satellite observations
#     are unavailable.
#     """

#     return {
#         "available": False,

#         "source": None,

#         "acquisition_window_days": None,

#         "ndvi": None,

#         "ndmi": None,

#         "bsi": None,

#         "cloud_masked": False,
#     }


# # =========================================================
# # CONFIGURATION
# # =========================================================

# def satellite_is_configured() -> bool:
#     """
#     Satellite integration is intentionally disabled.

#     This keeps the current project completely free and
#     avoids requiring any commercial satellite API account.
#     """

#     return False


# # =========================================================
# # MAIN FUNCTION
# # =========================================================

# async def get_satellite_indicators(
#     boundary: dict,
# ) -> dict[str, Any]:
#     """
#     Return satellite indicators for a farm.

#     Current implementation:

#         No external satellite API.

#     Therefore:

#         available = False

#         ndvi = None
#         ndmi = None
#         bsi = None

#     The rest of the application continues normally.
#     """

#     # -----------------------------------------------------
#     # Validate the GeoJSON boundary.
#     # -----------------------------------------------------

#     if (
#         not boundary
#         or boundary.get("type") != "Polygon"
#     ):
#         return get_empty_satellite_result()


#     # -----------------------------------------------------
#     # Satellite integration is currently disabled.
#     # -----------------------------------------------------

#     return get_empty_satellite_result()

import logging
from typing import Any

logger = logging.getLogger("krishimap.satellite")


# ============================================================================
# CONSTANTS
# ============================================================================

SUPPORTED_GEOMETRY_TYPES = {
    "Polygon",
    "MultiPolygon",
}


# ============================================================================
# EMPTY / FALLBACK RESULT
# ============================================================================

def get_empty_satellite_result() -> dict[str, Any]:
    """
    Return the stable satellite response used when no satellite provider
    is configured or satellite data is unavailable.

    Keep these keys stable because the recommendation service and frontend
    depend on this structure.
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


# ============================================================================
# CONFIGURATION
# ============================================================================

def satellite_is_configured() -> bool:
    """
    Check whether a real satellite provider has been configured.

    This intentionally returns False until an actual provider is connected.
    """
    return False


# ============================================================================
# GEOJSON VALIDATION
# ============================================================================

def _validate_boundary(
    boundary: dict[str, Any],
) -> None:
    """
    Validate the minimum GeoJSON structure required by the satellite layer.
    """

    if not isinstance(boundary, dict):
        raise ValueError(
            "Farm boundary must be a GeoJSON object."
        )

    geometry_type = boundary.get("type")

    if geometry_type not in SUPPORTED_GEOMETRY_TYPES:
        raise ValueError(
            "Farm boundary must be a Polygon or MultiPolygon."
        )

    coordinates = boundary.get("coordinates")

    if not coordinates:
        raise ValueError(
            "Farm boundary is missing coordinates."
        )

    if not isinstance(coordinates, list):
        raise ValueError(
            "Farm boundary coordinates must be a list."
        )


# ============================================================================
# SATELLITE INDICATORS
# ============================================================================

async def get_satellite_indicators(
    boundary: dict[str, Any],
) -> dict[str, Any]:
    """
    Retrieve satellite-derived agricultural indicators.

    Current behavior:
        - validates the farm boundary
        - returns the stable empty result because no satellite provider
          has been configured yet

    Future providers such as Sentinel-2, Landsat, Google Earth Engine,
    Sentinel Hub, or another remote-sensing API can be implemented here
    without changing the recommendation endpoint.
    """

    try:
        _validate_boundary(boundary)

    except ValueError:
        raise

    except Exception as exc:
        logger.exception(
            "Unexpected satellite boundary validation error: %s",
            exc,
        )
        raise ValueError(
            "Invalid farm boundary."
        )

    if not satellite_is_configured():
        return get_empty_satellite_result()

    # ------------------------------------------------------------------------
    # Future satellite provider integration
    # ------------------------------------------------------------------------
    #
    # Example architecture:
    #
    # 1. Extract farm geometry.
    # 2. Calculate bounding box.
    # 3. Query satellite provider.
    # 4. Apply cloud filtering.
    # 5. Calculate NDVI / NDMI / BSI.
    # 6. Aggregate values over the farm polygon.
    # 7. Return the stable response structure.
    #
    # Do not perform provider calls here until the provider credentials and
    # implementation are actually configured.
    # ------------------------------------------------------------------------

    return get_empty_satellite_result()