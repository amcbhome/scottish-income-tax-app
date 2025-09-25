from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class BandResult:
    name: str
    rate: float
    band_taxable: float
    tax: float

@dataclass
class TaxResult:
    tax_year: str
    gross_income: float
    personal_allowance: float
    taxable_income: float
    total_tax: float
    effective_rate: float
    band_breakdown: List[BandResult]
    notes: List[str]

class ScottishIncomeTax:
    """
    Scottish Income Tax calculator for non-savings, non-dividend (NSND) income.
    Tax year: 2025/26 (6 Apr 2025 – 5 Apr 2026).

    Scope:
      • Applies Scottish rates to NSND income only.
      • Uses UK Personal Allowance (PA) £12,570 with taper above £100,000
        (£1 reduction per £2; PA fully withdrawn by £125,140).
      • Excludes savings/dividend rates, NI, student loans, marriage allowance transfers,
        and relief-at-source adjustments (gift aid/pensions).
    """

    TAX_YEAR = "2025/26"

    # Scottish bands for 2025/26 as widths on taxable income (post-PA)
    BAND_WIDTHS: List[Tuple[str, float, float]] = [
        ("Starter",      0.19,  2827.0),   # 12,571–15,397
        ("Basic",        0.20, 12094.0),   # 15,398–27,491
        ("Intermediate", 0.21, 16171.0),   # 27,492–43,662
        ("Higher",       0.42, 31338.0),   # 43,663–75,000
        ("Advanced",     0.45, 50140.0),   # 75,001–125,140
        ("Top",          0.48, float("inf")),
    ]

    PA_STANDARD = 12570.0
    PA_TAPER_START = 100000.0
    PA_ZERO_POINT = 125140.0  # PA becomes 0 by this income level

    @staticmethod
    def tapered_personal_allowance(income: float) -> float:
        pa = ScottishIncomeTax.PA_STANDARD
        if income <= ScottishIncomeTax.PA_TAPER_START:
            return pa
        reduction = (income - ScottishIncomeTax.PA_TAPER_START) / 2.0
        return max(0.0, pa - reduction)

    @classmethod
    def calculate(cls, gross_income: float) -> TaxResult:
        pa = cls.tapered_personal_allowance(gross_income)
        taxable = max(0.0, gross_income - pa)

        remaining = taxable
        breakdown: List[BandResult] = []
        total_tax = 0.0

        for name, rate, width in cls.BAND_WIDTHS:
            if remaining <= 0:
                breakdown.append(BandResult(name, rate, 0.0, 0.0))
                continue
            take = remaining if width == float("inf") else min(remaining, width)
            band_tax = take * rate
            breakdown.append(BandResult(name, rate, take, band_tax))
            total_tax += band_tax
            remaining -= take

        effective_rate = (total_tax / gross_income * 100.0) if gross_income > 0 else 0.0

        notes = [
            f"Personal Allowance used: £{pa:,.0f}.",
            "Scottish bands apply only to non-savings, non-dividend income.",
            f"PA tapers £1 per £2 above £{cls.PA_TAPER_START:,.0f}; fully withdrawn by £{cls.PA_ZERO_POINT:,.0f}.",
        ]

        return TaxResult(
            tax_year=cls.TAX_YEAR,
            gross_income=round(gross_income, 2),
            personal_allowance=round(pa, 2),
            taxable_income=round(taxable, 2),
            total_tax=round(total_tax, 2),
            effective_rate=round(effective_rate, 2),
            band_breakdown=breakdown,
            notes=notes
        )
