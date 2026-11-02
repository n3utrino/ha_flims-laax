"""Client for the public Flims Laax live feed."""

import asyncio
import socket
from typing import Any

import aiohttp

from custom_components.flims_laax.const import LIVE_FEED_URL

REQUEST_TIMEOUT = 10


class FlimsLaaxApiClientError(Exception):
    """Base exception to indicate a general API error."""


class FlimsLaaxApiClientCommunicationError(FlimsLaaxApiClientError):
    """Exception to indicate a communication error with the API."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the API response is valid."""
    response.raise_for_status()


class FlimsLaaxApiClient:
    """Fetch and validate the public resort live feed."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._session = session

    async def async_get_data(self) -> dict[str, Any]:
        """Fetch the current resort data."""
        response = await self._api_wrapper(method="get", url=LIVE_FEED_URL)
        if response.get("status") != "success" or not isinstance(response.get("data"), dict):
            raise FlimsLaaxApiClientError("The live feed returned an invalid response")

        data = response["data"]
        if not isinstance(data.get("overview"), dict) or not isinstance(data.get("lifts"), list):
            raise FlimsLaaxApiClientError("The live feed is missing required resort data")

        return {
            "model": "Flims Laax live feed",
            "serial_number": "flims-laax",
            "sw_version": "live",
            "overview": data["overview"],
            "lifts": data["lifts"],
            "weather": data.get("weather", {}),
            "avalanche": data.get("avalanche", {}),
            "visitors": data.get("visitors", {}),
            "gate_counts": data.get("gateCounts", {}),
            "seasons": data.get("seasons", {}),
        }

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Perform a request and translate transport errors into client errors."""
        try:
            async with asyncio.timeout(REQUEST_TIMEOUT):
                async with self._session.request(method=method, url=url, json=data) as response:
                    _verify_response_or_raise(response)
                    payload = await response.json()
                    if not isinstance(payload, dict):
                        raise FlimsLaaxApiClientError("The live feed did not return a JSON object")
                    return payload
        except TimeoutError as exception:
            raise FlimsLaaxApiClientCommunicationError("Timed out fetching the live feed") from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise FlimsLaaxApiClientCommunicationError("Could not fetch the live feed") from exception
