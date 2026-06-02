"""SSRF guard for the HLS proxy.

Always blocks URLs that resolve to private / loopback / link-local / reserved /
metadata addresses (the critical control — prevents reaching internal services
or the cloud metadata endpoint). Optionally restricts to an allowlist of hosts
when ``STREAM_ENFORCE_ALLOWLIST`` is on.
"""
import asyncio
import ipaddress
from urllib.parse import urlsplit

from ssmarttv.core.config import settings
from ssmarttv.core.exceptions import AppError, PermissionDeniedError


def _is_blocked_ip(ip_str: str) -> bool:
    ip = ipaddress.ip_address(ip_str)
    return (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_reserved
        or ip.is_unspecified
    )


async def _resolve_ips(host: str) -> list[str]:
    loop = asyncio.get_running_loop()
    try:
        infos = await loop.getaddrinfo(host, None)
    except OSError as exc:
        raise PermissionDeniedError("Stream host could not be resolved") from exc
    return [info[4][0] for info in infos]


async def validate_target(url: str, *, allowed_hosts: set[str] | None = None) -> str:
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https"):
        raise AppError("Only http(s) stream URLs are allowed", code="invalid_stream_url")
    host = parts.hostname
    if not host:
        raise AppError("Stream URL has no host", code="invalid_stream_url")

    if settings.STREAM_ENFORCE_ALLOWLIST and (
        not allowed_hosts or host not in allowed_hosts
    ):
        raise PermissionDeniedError(f"Host '{host}' is not in the stream allowlist")

    for ip in await _resolve_ips(host):
        if _is_blocked_ip(ip):
            raise PermissionDeniedError("Stream host resolves to a blocked address")
    return url
