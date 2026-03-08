import re
from typing import Optional
from ..config import config


def _domain_pattern_to_regex(pattern: str) -> re.Pattern:
    """
    Converts a domain pattern with {0} and {1} placeholders into a regex
    that captures those placeholder values.
    e.g. "nn-{0}-{1}-ls-assets.rustyraven.pw" becomes /^nn-(.+?)-(.+?)-ls-assets\\.rustyraven\\.pw$/
    """
    # Escape regex special chars (except our placeholders)
    escaped = re.escape(pattern)
    # re.escape will turn {0} into \\{0\\} - we need to replace those back
    escaped = escaped.replace(r"\{0\}", "(.+?)")
    escaped = escaped.replace(r"\{1\}", "(.+?)")
    return re.compile("^" + escaped + "$")


# Pre-compile regexes for the asset domains
_assetbundle_url_regex = _domain_pattern_to_regex(config.domains.assetbundleUrl)
_assetbundle_info_url_regex = _domain_pattern_to_regex(config.domains.assetbundleInfoUrl)


class AssetDomainMatch:
    def __init__(self, type: str, placeholders: Optional[dict] = None):
        self.type = type
        self.placeholders = placeholders


def match_asset_domain(hostname: str) -> Optional[AssetDomainMatch]:
    """
    Match a hostname against the configured asset domains.
    Returns which domain type matched and, for assetbundleUrl/assetbundleInfoUrl,
    extracts the {0} and {1} placeholder values.
    """
    # Check exact match for assetbundleApi first
    if hostname == config.domains.assetbundleApi:
        return AssetDomainMatch(type="assetbundleApi")

    # Check assetbundleUrl pattern (has {0} and {1})
    url_match = _assetbundle_url_regex.match(hostname)
    if url_match:
        return AssetDomainMatch(
            type="assetbundleUrl",
            placeholders={"0": url_match.group(1), "1": url_match.group(2)},
        )

    # Check assetbundleInfoUrl pattern (has {0} and {1})
    info_match = _assetbundle_info_url_regex.match(hostname)
    if info_match:
        return AssetDomainMatch(
            type="assetbundleInfoUrl",
            placeholders={"0": info_match.group(1), "1": info_match.group(2)},
        )

    return None
