# Анализ уязвимостей образа `app:latest`

Сводка сканирования: **всего 4** (**HIGH: 2**, **CRITICAL: 2**).

---

**Total:** 21 (**HIGH:** 21, **CRITICAL:** 0)
| Library | Vulnerability | Severity | Status | Installed Version | Fixed Version | Title |
|---|---|---|---|---|---|---|
| libexpat1 | CVE-2026-25210 | HIGH | affected | 2.7.1-2 | — | libexpat: Information disclosure and data integrity issues due to integer overflow ([link](https://avd.aquasec.com/nvd/cve-2026-25210)) |
| libpython3.13-minimal | CVE-2025-13836 | HIGH | affected | 3.13.5-2 | — | cpython: Excessive read buffering DoS in http.client ([link](https://avd.aquasec.com/nvd/cve-2025-13836)) |
| libpython3.13-minimal | CVE-2025-15366 | HIGH | affected | 3.13.5-2 | — | cpython: IMAP command injection in user-controlled commands ([link](https://avd.aquasec.com/nvd/cve-2025-15366)) |
| libpython3.13-minimal | CVE-2025-15367 | HIGH | affected | 3.13.5-2 | — | cpython: POP3 command injection in user-controlled commands ([link](https://avd.aquasec.com/nvd/cve-2025-15367)) |
| libpython3.13-minimal | CVE-2025-8194 | HIGH | affected | 3.13.5-2 | — | cpython: Infinite loop when parsing a tarfile ([link](https://avd.aquasec.com/nvd/cve-2025-8194)) |
| libpython3.13-minimal | CVE-2026-1299 | HIGH | affected | 3.13.5-2 | — | cpython: Email header injection due to unquoted newlines ([link](https://avd.aquasec.com/nvd/cve-2026-1299)) |
| libpython3.13-stdlib | CVE-2025-13836 | HIGH | affected | 3.13.5-2 | — | cpython: Excessive read buffering DoS in http.client ([link](https://avd.aquasec.com/nvd/cve-2025-13836)) |
| libpython3.13-stdlib | CVE-2025-15366 | HIGH | affected | 3.13.5-2 | — | cpython: IMAP command injection in user-controlled commands ([link](https://avd.aquasec.com/nvd/cve-2025-15366)) |
| libpython3.13-stdlib | CVE-2025-15367 | HIGH | affected | 3.13.5-2 | — | cpython: POP3 command injection in user-controlled commands ([link](https://avd.aquasec.com/nvd/cve-2025-15367)) |
| libpython3.13-stdlib | CVE-2025-8194 | HIGH | affected | 3.13.5-2 | — | cpython: Infinite loop when parsing a tarfile ([link](https://avd.aquasec.com/nvd/cve-2025-8194)) |
| libpython3.13-stdlib | CVE-2026-1299 | HIGH | affected | 3.13.5-2 | — | cpython: Email header injection due to unquoted newlines ([link](https://avd.aquasec.com/nvd/cve-2026-1299)) |
| python3.13-minimal | CVE-2025-13836 | HIGH | affected | 3.13.5-2 | — | cpython: Excessive read buffering DoS in http.client ([link](https://avd.aquasec.com/nvd/cve-2025-13836)) |
| python3.13-minimal | CVE-2025-15366 | HIGH | affected | 3.13.5-2 | — | cpython: IMAP command injection in user-controlled commands ([link](https://avd.aquasec.com/nvd/cve-2025-15366)) |
| python3.13-minimal | CVE-2025-15367 | HIGH | affected | 3.13.5-2 | — | cpython: POP3 command injection in user-controlled commands ([link](https://avd.aquasec.com/nvd/cve-2025-15367)) |
| python3.13-minimal | CVE-2025-8194 | HIGH | affected | 3.13.5-2 | — | cpython: Infinite loop when parsing a tarfile ([link](https://avd.aquasec.com/nvd/cve-2025-8194)) |
| python3.13-minimal | CVE-2026-1299 | HIGH | affected | 3.13.5-2 | — | cpython: Email header injection due to unquoted newlines ([link](https://avd.aquasec.com/nvd/cve-2026-1299)) |
| python3.13-venv | CVE-2025-13836 | HIGH | affected | 3.13.5-2 | — | cpython: Excessive read buffering DoS in http.client ([link](https://avd.aquasec.com/nvd/cve-2025-13836)) |
| python3.13-venv | CVE-2025-15366 | HIGH | affected | 3.13.5-2 | — | cpython: IMAP command injection in user-controlled commands ([link](https://avd.aquasec.com/nvd/cve-2025-15366)) |
| python3.13-venv | CVE-2025-15367 | HIGH | affected | 3.13.5-2 | — | cpython: POP3 command injection in user-controlled commands ([link](https://avd.aquasec.com/nvd/cve-2025-15367)) |
| python3.13-venv | CVE-2025-8194 | HIGH | affected | 3.13.5-2 | — | cpython: Infinite loop when parsing a tarfile ([link](https://avd.aquasec.com/nvd/cve-2025-8194)) |
| python3.13-venv | CVE-2026-1299 | HIGH | affected | 3.13.5-2 | — | cpython: Email header injection due to unquoted newlines ([link](https://avd.aquasec.com/nvd/cve-2026-1299)) |

казанные уязвимости относятся к системным пакетам базового образа gcr.io/distroless/python3-debian13:nonroot, для их устранения нужно регулярно обновлять базовый образ и пересобирать с ним образ приложения.