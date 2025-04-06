# WildMediaServer 🎬

**Python Media Server** - Vue.js Frontend with MySQL Backend

[![Contributing Guidelines](https://img.shields.io/badge/Contributing-3.0-blue.svg)](CONTRIBUTING.md)
[![Code of Conduct](https://img.shields.io/badge/CoC-2.1-ff69b4.svg)](CODE_OF_CONDUCT.md)

## 📜 License
GNU GPLv3 - See [LICENSE](LICENSE) for details.

> **Important Links**  
> 🔗 [Contribution Guidelines](CONTRIBUTING.md)  
> 🔗 [Code of Conduct](CODE_OF_CONDUCT.md)

## 🤝 Contribution Requirements
```python
# Pseudocode validation
if not (pr.meets_performance_metrics and 
        pr.has_approved_issue and
        pr.follows_coc):
    reject()
```

## 🛠 Development Setup
```bash
# Install with policy checks
git clone https://github.com/Vyx-Software/WildMediaServer.git
cd WildMediaServer
./install.sh --verify-policies
```

## ❗ Enforcement Flow
```mermaid
graph LR
    A[PR Submitted] --> B{Validates Against<br>CONTRIBUTING.md?}
    B -->|Yes| C{Complies With<br>CODE_OF_CONDUCT.md?}
    B -->|No| D[Rejected]
    C -->|Yes| E[Approved]
    C -->|No| F[Rejected]
```
