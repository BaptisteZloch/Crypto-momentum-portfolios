from typing import Dict, List


def capi_weighted_allocation(
    selected_assets: List[str], selected_assets_capi: List[float]
) -> Dict[str, float]:
    return {
        asset: selected_assets_capi[i] / sum(selected_assets_capi)
        for i, asset in enumerate(selected_assets)
    }


def volume_weighted_allocation(
    selected_assets: List[str], selected_assets_volume: List[float]
) -> Dict[str, float]:
    return {
        asset: selected_assets_volume[i] / sum(selected_assets_volume)
        for i, asset in enumerate(selected_assets)
    }


def equal_weighted_allocation(selected_assets: List[str]) -> Dict[str, float]:
    return {asset: 1 / len(selected_assets) for asset in selected_assets}
