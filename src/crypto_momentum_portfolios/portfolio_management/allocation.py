from copy import copy
from enum import StrEnum
from typing import Any, Callable, Dict, List
import numpy as np
import numpy.typing as npt
import pandas as pd

from scipy.optimize import minimize

from crypto_momentum_portfolios.utility.types import AllocationMethod, Fields


class Allocation:
    @staticmethod
    def capitalization_weighted_allocation(
        selected_assets: List[str],
        selected_assets_capitalization: pd.DataFrame,
        *arg,
        **kwargs
    ) -> Dict[str, float]:
        selected_assets_capi = (
            selected_assets_capitalization[selected_assets].iloc[-1].to_list()
        )
        return {
            asset: selected_assets_capi[i] / sum(selected_assets_capi)
            for i, asset in enumerate(selected_assets)
        }

    @staticmethod
    def volume_weighted_allocation(
        selected_assets: List[str], selected_assets_volume: pd.DataFrame, *arg, **kwargs
    ) -> Dict[str, float]:
        volume = selected_assets_volume[selected_assets].iloc[-1].to_list()
        return {
            asset: volume[i] / sum(volume) for i, asset in enumerate(selected_assets)
        }

    @staticmethod
    def equal_weighted_allocation(
        selected_assets: List[str], *arg, **kwargs
    ) -> Dict[str, float]:
        return {asset: 1 / len(selected_assets) for asset in selected_assets}

    @staticmethod
    def momentum_weighted_allocation(
        selected_assets: List[str], selected_assets_mom: pd.DataFrame
    ) -> Dict[str, float]:
        mom = selected_assets_mom[selected_assets].iloc[-1].to_list()
        return {asset: mom[i] / sum(mom) for i, asset in enumerate(selected_assets)}

    @staticmethod
    def risk_parity_allocation(
        selected_assets: List[str],
        selected_assets_returns: pd.DataFrame,
        *arg,
        **kwargs
    ) -> Dict[str, float]:
        def risk_budget_objective(weights: npt.NDArray[np.float32], arg: List[Any]):
            v = arg[0]
            risk_budget = arg[1]
            # Risk of the portfolio
            sigma_p = np.sqrt(weights @ v @ weights.T)
            # Marginal contribution of each asset to the risk of the portfolio
            marginal_risk_contribution = v * weights.T
            # Contribution of each asset to the risk of the portfolio
            assets_risk_contribution = (
                marginal_risk_contribution @ weights.T
            ) / sigma_p  # * 252

            # We calculate the desired contribution of each asset to the risk of the weights distribution
            assets_risk_target = sigma_p * risk_budget

            # Error between the desired contribution and the calculated contribution of each asset
            residual = assets_risk_contribution - assets_risk_target
            return residual @ residual.T

        w0 = np.array([1 / len(selected_assets) for _ in selected_assets])
        budget = copy(w0)

        cons = (
            {
                "type": "eq",
                "fun": lambda weights: np.sum(weights) - 1,
            },  # return 0 if sum of the weights is 1
            {"type": "ineq", "fun": lambda x: x},  # Long only
        )

        bounds = tuple([(0.0, 1.0) for _ in selected_assets])
        weights = minimize(
            risk_budget_objective,
            x0=w0,
            args=[selected_assets_returns.cov().to_numpy(), budget],
            method="SLSQP",
            constraints=cons,
            bounds=bounds,
            options={"disp": False},
            tol=1e-10,
        ).x
        return {
            security: unit_weight
            for security, unit_weight in zip(
                selected_assets,
                weights,
            )
        }

    @staticmethod
    def mean_variance_allocation(
        selected_assets: List[str],
        selected_assets_returns: pd.DataFrame,
        *arg,
        **kwargs
    ) -> Dict[str, float]:
        def mean_variance_objective(weights: npt.NDArray[np.float32], arg: List[Any]):
            cov_matrix = arg[0]
            expected_return_vector = arg[1]
            # rf = float(arg[2])
            # Risk of the portfolio
            sigma_p = np.sqrt(weights @ cov_matrix @ weights.T)
            expected_return = expected_return_vector @ weights.T
            return -expected_return / sigma_p

        w0 = np.array([1 / len(selected_assets) for _ in selected_assets])
        budget = copy(w0)

        cons = (
            {
                "type": "eq",
                "fun": lambda weights: np.sum(weights) - 1,
            },  # return 0 if sum of the weights is 1
            {"type": "ineq", "fun": lambda x: x},  # Long only
        )

        bounds = tuple([(0.0, 1.0) for _ in selected_assets])
        weights = minimize(
            mean_variance_objective,
            x0=w0,
            args=[
                selected_assets_returns.cov().to_numpy(),
                selected_assets_returns.mean().to_numpy(),
            ],
            method="SLSQP",
            constraints=cons,
            bounds=bounds,
            options={"disp": False},
            tol=1e-10,
        ).x
        return {
            security: unit_weight
            for security, unit_weight in zip(
                selected_assets,
                weights,
            )
        }


ALLOCATION_TO_FUNCTION: Dict[
    AllocationMethod, Callable[[List[str], pd.DataFrame], Dict[str, float]]
] = {
    AllocationMethod.CAPITALIZATION_WEIGHTED: Allocation.capitalization_weighted_allocation,
    AllocationMethod.VOLUME_WEIGHTED: Allocation.volume_weighted_allocation,
    AllocationMethod.EQUAL_WEIGHTED: Allocation.equal_weighted_allocation,
    AllocationMethod.MOMENTUM_WEIGHTED: Allocation.momentum_weighted_allocation,
    AllocationMethod.RISK_PARITY: Allocation.risk_parity_allocation,
    AllocationMethod.MEAN_VARIANCE: Allocation.mean_variance_allocation,
}

ALLOCATION_FIELDS: Dict[AllocationMethod, Fields] = {
    AllocationMethod.CAPITALIZATION_WEIGHTED: Fields.MARKET_CAP,
    AllocationMethod.VOLUME_WEIGHTED: Fields.VOLUME,
    AllocationMethod.EQUAL_WEIGHTED: Fields.RETURNS,
    AllocationMethod.MOMENTUM_WEIGHTED: Fields.MOMENTUM,
    AllocationMethod.RISK_PARITY: Fields.RETURNS,
    AllocationMethod.MEAN_VARIANCE: Fields.RETURNS,
}
