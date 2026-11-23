#!/usr/bin/env python3
"""Estimador conservador de rescisão CLT para planejamento mensal.

Não substitui TRCT, contador, sindicato ou advogado. Usa regras/tabelas 2026
registradas no SKILL.md e deve ser revisado quando a legislação mudar.
"""

from __future__ import annotations

import argparse
import calendar
import json
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

D = Decimal
CENT = D("0.01")


def money(v: Decimal) -> str:
    return f"{v.quantize(CENT, rounding=ROUND_HALF_UP)}"


def dec(value, default="0") -> Decimal:
    if value in (None, ""):
        return D(default)
    return D(str(value))


def parse_date(value: str) -> date:
    return date.fromisoformat(value)


def add_months(d: date, months: int) -> date:
    total = d.year * 12 + d.month - 1 + months
    year, month0 = divmod(total, 12)
    month = month0 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def completed_years(start: date, end: date) -> int:
    years = end.year - start.year
    try:
        anniversary = start.replace(year=end.year)
    except ValueError:
        anniversary = start.replace(year=end.year, day=28)
    return years - (end < anniversary)


def notice_days(admission: date, termination: date) -> int:
    # Entendimento operacional: 30 dias até completar 1 ano e +3 por ano
    # completo, limitado a 90 dias. Conferir CCT e entendimento vigente.
    return min(90, 30 + 3 * max(0, completed_years(admission, termination)))


def overlap_days(a_start: date, a_end: date, b_start: date, b_end: date) -> int:
    start = max(a_start, b_start)
    end = min(a_end, b_end)
    return max(0, (end - start).days + 1)


def thirteenth_avos(admission: date, end: date) -> int:
    start = max(admission, date(end.year, 1, 1))
    if start > end:
        return 0
    avos = 0
    for month in range(1, 13):
        m_start = date(end.year, month, 1)
        m_end = date(end.year, month, calendar.monthrange(end.year, month)[1])
        if overlap_days(start, end, m_start, m_end) >= 15:
            avos += 1
    return min(12, avos)


def vacation_avos(period_start: date, end: date) -> int:
    if end < period_start:
        return 0
    avos = 0
    cursor = period_start
    for _ in range(12):
        next_cursor = add_months(cursor, 1)
        full_period_end = next_cursor - timedelta(days=1)
        days = overlap_days(period_start, end, cursor, full_period_end)
        if days >= 15:
            avos += 1
        cursor = next_cursor
        if cursor > end:
            break
    return min(12, avos)


# Tabela progressiva INSS para empregado — competência 2026.
INSS_BANDS = [
    (D("1621.00"), D("0.075")),
    (D("2902.84"), D("0.09")),
    (D("4354.27"), D("0.12")),
    (D("8475.55"), D("0.14")),
]


def inss_2026(amount: Decimal) -> Decimal:
    amount = max(D("0"), amount)
    total = D("0")
    lower = D("0")
    for upper, rate in INSS_BANDS:
        slice_value = min(amount, upper) - lower
        if slice_value > 0:
            total += slice_value * rate
        lower = upper
        if amount <= upper:
            break
    return total.quantize(CENT, rounding=ROUND_HALF_UP)


IR_BANDS = [
    (D("2428.80"), D("0"), D("0")),
    (D("2826.65"), D("0.075"), D("182.16")),
    (D("3751.05"), D("0.15"), D("394.16")),
    (D("4664.68"), D("0.225"), D("675.49")),
    (D("999999999"), D("0.275"), D("908.73")),
]


def irrf_2026(gross_taxable: Decimal, inss: Decimal, dependents: int) -> Decimal:
    legal_deduction = D("189.59") * D(dependents)
    simplified = D("607.20")
    chosen_deduction = max(legal_deduction, simplified)
    base = max(D("0"), gross_taxable - inss - chosen_deduction)
    tax = D("0")
    for upper, rate, deduction in IR_BANDS:
        if base <= upper:
            tax = max(D("0"), base * rate - deduction)
            break

    # Redução mensal instituída para 2026.
    if gross_taxable <= D("5000.00"):
        reduction = min(tax, D("312.89"))
    elif gross_taxable <= D("7350.00"):
        reduction = max(D("0"), D("978.62") - D("0.133145") * gross_taxable)
    else:
        reduction = D("0")
    return max(D("0"), tax - reduction).quantize(CENT, rounding=ROUND_HALF_UP)


@dataclass
class Inputs:
    monthly_salary: Decimal
    variable_average: Decimal
    admission_date: date
    termination_date: date
    days_worked: int
    current_vacation_period_start: date
    acquired_vacation_periods: int
    double_vacation_periods: int
    fgts_termination_base: Decimal
    fgts_current_balance: Decimal
    fgts_mode: str
    dependents: int
    thirteenth_advance: Decimal
    other_deductions: Decimal
    cost_of_living: Decimal

    @property
    def remuneration(self) -> Decimal:
        return self.monthly_salary + self.variable_average


def load_inputs(path: Path) -> Inputs:
    raw = json.loads(path.read_text())
    required = [
        "monthly_salary",
        "admission_date",
        "termination_date",
        "current_vacation_period_start",
    ]
    missing = [key for key in required if raw.get(key) in (None, "")]
    if missing:
        raise ValueError("Campos obrigatórios ausentes: " + ", ".join(missing))
    return Inputs(
        monthly_salary=dec(raw["monthly_salary"]),
        variable_average=dec(raw.get("variable_average")),
        admission_date=parse_date(raw["admission_date"]),
        termination_date=parse_date(raw["termination_date"]),
        days_worked=int(raw.get("days_worked_in_termination_month", raw["termination_date"][-2:])),
        current_vacation_period_start=parse_date(raw["current_vacation_period_start"]),
        acquired_vacation_periods=int(raw.get("acquired_vacation_periods", 0)),
        double_vacation_periods=int(raw.get("double_vacation_periods", 0)),
        fgts_termination_base=dec(raw.get("fgts_termination_base")),
        fgts_current_balance=dec(raw.get("fgts_current_balance")),
        fgts_mode=str(raw.get("fgts_mode", "unknown")),
        dependents=int(raw.get("dependents", 0)),
        thirteenth_advance=dec(raw.get("thirteenth_advance")),
        other_deductions=dec(raw.get("other_deductions")),
        cost_of_living=dec(raw.get("cost_of_living_monthly", "9000")),
    )


def common_components(i: Inputs, effective_end: date) -> dict[str, Decimal | int]:
    remuneration = i.remuneration
    salary_balance = remuneration / D("30") * D(min(30, max(0, i.days_worked)))
    avos_13 = thirteenth_avos(i.admission_date, effective_end)
    thirteenth = max(D("0"), remuneration * D(avos_13) / D("12") - i.thirteenth_advance)
    vac_avos = vacation_avos(i.current_vacation_period_start, effective_end)
    acquired_normal = remuneration * D(i.acquired_vacation_periods) * D("4") / D("3")
    acquired_double = remuneration * D(i.double_vacation_periods) * D("2") * D("4") / D("3")
    proportional_vacation = remuneration * D(vac_avos) / D("12") * D("4") / D("3")
    return {
        "salary_balance": salary_balance,
        "thirteenth_avos": avos_13,
        "thirteenth": thirteenth,
        "vacation_avos": vac_avos,
        "acquired_vacation": acquired_normal,
        "double_vacation": acquired_double,
        "proportional_vacation": proportional_vacation,
    }


def estimate_taxes(i: Inputs, salary_balance: Decimal, thirteenth: Decimal) -> dict[str, Decimal]:
    inss_salary = inss_2026(salary_balance)
    ir_salary = irrf_2026(salary_balance, inss_salary, i.dependents)
    inss_13 = inss_2026(thirteenth)
    ir_13 = irrf_2026(thirteenth, inss_13, i.dependents)
    return {
        "inss_salary": inss_salary,
        "irrf_salary": ir_salary,
        "inss_thirteenth": inss_13,
        "irrf_thirteenth": ir_13,
        "total": inss_salary + ir_salary + inss_13 + ir_13,
    }


def scenario(i: Inputs, kind: str) -> dict:
    remuneration = i.remuneration
    notice = D("0")
    notice_deduction = D("0")
    notice_days_value = 0
    effective_end = i.termination_date
    fgts_penalty_rate = D("0")

    if kind == "dismissal_without_cause":
        notice_days_value = notice_days(i.admission_date, i.termination_date)
        notice = remuneration / D("30") * D(notice_days_value)
        effective_end = i.termination_date + timedelta(days=notice_days_value)
        fgts_penalty_rate = D("0.40")
    elif kind == "mutual_agreement":
        notice_days_value = notice_days(i.admission_date, i.termination_date)
        notice = remuneration / D("30") * D(notice_days_value) / D("2")
        effective_end = i.termination_date + timedelta(days=notice_days_value // 2)
        fgts_penalty_rate = D("0.20")
    elif kind == "resignation_no_notice":
        notice_deduction = remuneration
    elif kind != "resignation_notice_worked_or_waived":
        raise ValueError(f"Cenário desconhecido: {kind}")

    c = common_components(i, effective_end)
    salary_balance = c["salary_balance"]
    thirteenth = c["thirteenth"]
    gross_employer = (
        salary_balance
        + thirteenth
        + c["acquired_vacation"]
        + c["double_vacation"]
        + c["proportional_vacation"]
        + notice
    )
    deductions_other = i.other_deductions + notice_deduction
    taxes = estimate_taxes(i, salary_balance, thirteenth)
    employer_net = max(D("0"), gross_employer - deductions_other - taxes["total"])

    final_fgts_deposits = D("0")
    fgts_penalty = D("0")
    withdrawable_fgts = D("0")
    if kind in {"dismissal_without_cause", "mutual_agreement"}:
        final_fgts_deposits = D("0.08") * (salary_balance + thirteenth + notice)
        fgts_penalty = (i.fgts_termination_base + final_fgts_deposits) * fgts_penalty_rate
        account_estimate = i.fgts_current_balance + final_fgts_deposits
        if kind == "dismissal_without_cause":
            if i.fgts_mode == "saque-rescisao":
                withdrawable_fgts = account_estimate
            elif i.fgts_mode == "saque-aniversario":
                withdrawable_fgts = D("0")
        else:
            if i.fgts_mode == "saque-rescisao":
                withdrawable_fgts = account_estimate * D("0.80")
            elif i.fgts_mode == "saque-aniversario":
                withdrawable_fgts = D("0")

    accessible_total = employer_net + fgts_penalty + withdrawable_fgts
    runway = accessible_total / i.cost_of_living if i.cost_of_living > 0 else D("0")

    return {
        "scenario": kind,
        "termination_date": str(i.termination_date),
        "effective_end_with_notice_projection": str(effective_end),
        "notice_days": notice_days_value,
        "thirteenth_avos": c["thirteenth_avos"],
        "vacation_avos": c["vacation_avos"],
        "components": {
            "salary_balance": money(salary_balance),
            "thirteenth": money(thirteenth),
            "acquired_vacation_plus_one_third": money(c["acquired_vacation"]),
            "double_vacation_plus_one_third": money(c["double_vacation"]),
            "proportional_vacation_plus_one_third": money(c["proportional_vacation"]),
            "notice_indemnity": money(notice),
            "notice_deduction": money(notice_deduction),
            "other_deductions": money(i.other_deductions),
        },
        "gross_paid_by_employer": money(gross_employer),
        "estimated_taxes": {k: money(v) for k, v in taxes.items()},
        "estimated_net_paid_by_employer": money(employer_net),
        "fgts": {
            "mode": i.fgts_mode,
            "estimated_final_deposits": money(final_fgts_deposits),
            "termination_penalty": money(fgts_penalty),
            "estimated_withdrawable_balance": money(withdrawable_fgts),
        },
        "estimated_immediately_accessible_total": money(accessible_total),
        "runway_months_at_cost_of_living": money(runway),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    inputs = load_inputs(args.config)
    output = {
        "disclaimer": "Estimativa para planejamento; conferir CCT, extrato FGTS, TRCT e regras vigentes.",
        "cost_of_living_monthly": money(inputs.cost_of_living),
        "scenarios": [
            scenario(inputs, "resignation_notice_worked_or_waived"),
            scenario(inputs, "resignation_no_notice"),
            scenario(inputs, "dismissal_without_cause"),
            scenario(inputs, "mutual_agreement"),
        ],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
