# Compliance

This system was designed for deployment in South Africa (a 40+ branch retailer), which brings three regulatory regimes: POPIA for data protection, ICASA for radio-frequency hardware, and NRCS for hardware safety. This document records how each is addressed.

## POPIA — Protection of Personal Information Act

POPIA governs any customer-linked data. The design minimises personal-data exposure and protects what little is processed:

- **No raw PII in logs.** Lambda functions log item, device, and location identifiers — never customer-identifiable data.
- **Encryption at rest.** DynamoDB and S3 use AES-256 encryption for any data that could be linked to a customer.
- **Least-privilege access.** Each Lambda runs under an IAM role scoped to only the resources it needs; no broad permissions.
- **Auditability.** CloudTrail logs all access to data stores, supporting POPIA's accountability requirements.
- **Data residency.** Workloads run in the af-south-1 (Cape Town) region to keep data within South Africa.

## ICASA — Independent Communications Authority of South Africa

RFID hardware transmits over radio frequencies, which ICASA regulates.

- All RFID readers and tags operate in ICASA-certified frequency bands for South Africa.
- Type-approval certification cost: approximately ZAR 15,000–30,000 (one-time, per hardware model).

## NRCS — National Regulator for Compulsory Specifications

NRCS governs the safety of electronic hardware sold and operated in South Africa.

- RFID reader hardware undergoes NRCS safety testing and certification before deployment.
- Certification cost: approximately ZAR 90,000–360,000 depending on the number of hardware models.

## Summary

Compliance was treated as a design constraint from the outset, not an afterthought — data-protection controls are built into the architecture (encryption, least privilege, audit logging, data residency), and hardware certification costs were factored into the overall implementation budget documented in [DECISION_RECORD.md](../DECISION_RECORD.md).
