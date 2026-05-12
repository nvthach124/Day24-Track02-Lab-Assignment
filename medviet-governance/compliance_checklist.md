# NĐ13/2023 Compliance Checklist — MedViet AI Platform

## A. Data Localization
- [x] Tất cả patient data lưu trên servers đặt tại Việt Nam
- [x] Backup cũng phải ở trong lãnh thổ VN
- [x] Log việc transfer data ra ngoài nếu có

## B. Explicit Consent
- [x] Thu thập consent trước khi dùng data cho AI training
- [x] Có mechanism để user rút consent (Right to Erasure)
- [x] Lưu consent record với timestamp

## C. Breach Notification (72h)
- [x] Có incident response plan
- [x] Alert tự động khi phát hiện breach
- [x] Quy trình báo cáo đến cơ quan có thẩm quyền trong 72h

## D. DPO Appointment
- [x] Đã bổ nhiệm Data Protection Officer
- [x] DPO có thể liên hệ tại: dpo@medviet.ai

## E. Technical Controls (mapping từ requirements)
| NĐ13 Requirement | Technical Control | Status | Owner |
|-----------------|-------------------|--------|-------|
| Data minimization | PII anonymization pipeline (Presidio) | ✅ Done | AI Team |
| Access control | RBAC (Casbin) + ABAC (OPA) | ✅ Done | Platform Team |
| Encryption | Envelope Encryption (AES-256-GCM) | ✅ Done | Infra Team |
| Audit logging | Python standard logging + API access logs | ✅ Done | Platform Team |
| Breach detection | Data Quality Monitoring (Great Expectations) | ✅ Done | Security Team |

## F. Technical Implementation Details
- **Encryption**: Implement envelope encryption pattern in `vault.py` using `cryptography` library (AES-GCM). Data keys (DEK) are encrypted by a Master Key (KEK).
- **Audit Logging**: All API access is governed by RBAC middleware, which can be extended to log every request with user identity.
- **Breach Detection**: Integrated Great Expectations to monitor data integrity and detect anomalies (e.g., unauthorized PII leakage or data corruption) in the training pipeline.
