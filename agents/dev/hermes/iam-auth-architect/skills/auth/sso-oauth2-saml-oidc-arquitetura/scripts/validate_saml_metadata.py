#!/usr/bin/env python3
"""Validate a SAML 2.0 metadata XML file (stdlib only, no external dependencies).

Usage: python3 validate_saml_metadata.py <metadata.xml>
"""
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

NS = {
    "md": "urn:oasis:names:tc:SAML:2.0:metadata",
    "ds": "http://www.w3.org/2000/09/xmldsig#",
}


def parse_time(value: str) -> datetime:
    value = value.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def validate(path: str) -> int:
    findings = []
    warnings = []

    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        print(f"ERRO: XML malformado: {exc}")
        return 1

    root = tree.getroot()

    entity_descriptor = root if root.tag.endswith("EntityDescriptor") else root.find(
        "md:EntityDescriptor", NS
    )
    if entity_descriptor is None:
        findings.append("Nenhum elemento EntityDescriptor encontrado.")
    else:
        entity_id = entity_descriptor.get("entityID")
        if not entity_id:
            findings.append("EntityDescriptor sem atributo entityID.")
        else:
            print(f"entityID: {entity_id}")

        valid_until = entity_descriptor.get("validUntil") or root.get("validUntil")
        if valid_until:
            try:
                dt = parse_time(valid_until)
                now = datetime.now(timezone.utc)
                if dt < now:
                    findings.append(f"Metadata EXPIRADA (validUntil={valid_until}).")
                else:
                    days_left = (dt - now).days
                    print(f"validUntil: {valid_until} ({days_left} dias restantes)")
                    if days_left < 30:
                        warnings.append(
                            f"Metadata expira em menos de 30 dias ({days_left} dias)."
                        )
            except ValueError:
                warnings.append(f"validUntil presente mas em formato inesperado: {valid_until}")
        else:
            warnings.append("Sem atributo validUntil — considerar adicionar para rotação.")

    certs = root.findall(".//ds:X509Certificate", NS)
    if not certs:
        findings.append("Nenhum certificado X509Certificate encontrado (KeyDescriptor).")
    else:
        print(f"Certificados encontrados: {len(certs)}")

    slo = root.findall(".//md:SingleLogoutService", NS)
    if not slo:
        warnings.append(
            "Nenhum SingleLogoutService (SLO) encontrado — confirmar se é intencional."
        )
    else:
        print(f"SingleLogoutService endpoints: {len(slo)}")

    sso_or_acs = root.findall(".//md:SingleSignOnService", NS) + root.findall(
        ".//md:AssertionConsumerService", NS
    )
    if not sso_or_acs:
        warnings.append(
            "Nenhum SingleSignOnService (IdP) nem AssertionConsumerService (SP) encontrado."
        )

    print()
    if warnings:
        print("AVISOS:")
        for w in warnings:
            print(f"  - {w}")
    if findings:
        print("PROBLEMAS:")
        for f in findings:
            print(f"  - {f}")
        return 1

    print("OK: metadata SAML passou nas verificações básicas.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(validate(sys.argv[1]))
