"""Reference ICE and BEV models used by the training planner and tests."""

from dataclasses import dataclass
from math import copysign


@dataclass(frozen=True)
class IcePoint:
    throttle_pct: float
    rpm: float
    torque_nm: float
    bsfc_g_kwh: float


def ice_torque(throttle_pct: float, rpm: float) -> IcePoint:
    """Estimate ICE torque and BSFC for a normalized operating point."""
    throttle = max(0.0, min(100.0, throttle_pct))
    speed = max(0.0, rpm)
    speed_factor = max(0.25, 1.0 - abs(speed - 2500.0) / 5000.0)
    torque = round(280.0 * (throttle / 100.0) * speed_factor, 2)
    bsfc = round(220.0 + abs(speed - 2500.0) * 0.025 + (100.0 - throttle) * 0.35, 2)
    return IcePoint(throttle, speed, torque, bsfc)


@dataclass(frozen=True)
class BevPoint:
    torque_nm: float
    iq_a: float
    id_a: float
    electrical_power_kw: float


def pmsm_foc(torque_nm: float, rpm: float, kt_nm_per_a: float = 0.48) -> BevPoint:
    """Return a simplified id/iq FOC operating point for a surface PMSM."""
    if kt_nm_per_a <= 0:
        raise ValueError("kt_nm_per_a must be positive")
    torque = float(torque_nm)
    iq = torque / kt_nm_per_a
    electrical_power_kw = abs(torque * max(0.0, float(rpm)) * 2.0 * 3.141592653589793 / 60.0) / 1000.0
    return BevPoint(
        torque_nm=round(torque, 2),
        iq_a=round(iq, 2),
        id_a=0.0,
        electrical_power_kw=round(copysign(electrical_power_kw, torque), 2),
    )