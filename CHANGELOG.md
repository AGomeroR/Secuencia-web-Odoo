# Changelog

All notable changes to the Odoo Website Sequence Optimizer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-26

### Added
- Initial release of Odoo Website Sequence Optimizer
- Intelligent 4-tier priority system (Active+Published, Active, Published, Inactive)
- eCommerce readiness scoring (categories, images, descriptions)
- Sales performance tie-breaker integration
- Two-phase update mechanism to avoid sequence conflicts
- Dry-run mode for safe preview of changes
- Verbose logging mode for detailed execution insights
- Batch processing for large product datasets (500 products per batch)
- Comprehensive logging to file (website_sequence_optimization.log)
- JSON report generation with timestamped filenames
- API key authentication for Odoo XML-RPC connection
- Environment variable configuration via .env file
- Automatic permission verification before updates
- Error recovery and detailed error logging

### Features
- Processes ALL products (active and inactive) for complete optimization
- Calculates priority scores based on multiple criteria
- Real-time progress indicators with emoji feedback
- Detailed statistics and breakdown by status and criteria
- Preview of top priority products in verbose mode
- Support for databases with 10,000+ products

### Documentation
- Comprehensive README in Spanish (README_ES.md)
- Comprehensive README in English (README.md)
- Python dependencies specification (requirements.txt)
- Git ignore configuration (.gitignore)
- This changelog file (CHANGELOG.md)

### Author
Developed by Álvaro Gómez (gomex1994@gmail.com)

---

## Future Enhancements (Planned)

### Potential Features
- Scheduled execution support (cron integration)
- Email notifications for optimization runs
- Custom scoring weight configuration
- Multi-company support
- Category-specific optimization
- Export/import of optimization configurations
- Web UI dashboard for monitoring
- Performance metrics and analytics

---

**Note**: For bug reports, feature requests, or contributions, please contact gomex1994@gmail.com
