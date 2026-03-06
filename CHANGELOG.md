# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.4.0] - 2026-03-05

### Added
- **Configuration validation**: Invalid config values are now detected and auto-corrected with warnings
- **Test suite**: Comprehensive pytest tests for config, themes, flowables, and PDF generation
- `ConfigValidationError` exception for strict validation mode
- `requirements-dev.txt` for development dependencies

### Changed
- **Removed global state**: Theme colors now passed through constructors (improves testability and thread safety)
- Extracted spacing, sizing, and column width constants to `constants.py`
- Created `factories.py` with helper functions for form elements

### Improved
- Better error messages for invalid configuration values
- Code maintainability through dependency injection pattern

## [5.3.0] - 2026-03-03

### Changed
- **Default output path**: PDFs now save to `~/Downloads/` by default
- Output directory is automatically created if it doesn't exist
- Theme descriptions in skill.yaml prompt now show all 13 themes as numbered list

### Improved
- Documentation updated to reflect 13 available themes

## [5.2.0] - 2026-03-03

### Added
- **6 new color themes**: summer, neon, berry, fiery, blush, deepblue
- Total of 13 themes now available

## [5.1.0] - 2026-03-03

### Added
- **Section configuration system**: Override which sections appear in the form
- New CLI options: `--include-section`, `--exclude-section`, `--list-sections`
- Section defaults by service type (walking now minimal by default, can add sections as needed)
- Config file `sections:` block for persistent section overrides

### Changed
- Service type now sets sensible section defaults (walking excludes vaccinations/health/feeding by default)
- Deprecated `--no-home-access` in favor of `--exclude-section home_access`
- Updated example configs to demonstrate section overrides

## [5.0.0] - 2026-03-03

### Added
- ClawHub skill manifest (`clawhub.json`) for marketplace publishing
- Comprehensive `SKILL.md` for AI agent integration
- Screenshots directory for ClawHub listing
- Permission justification documentation

### Changed
- Updated README with troubleshooting section and permission documentation

## [4.0.0] - 2026-02-15

### Added
- Home access section (keys, codes, alarm, WiFi, parking)
- YAML config file support for business presets
- Example config files for boarding, walking, and in-home sitting
- `--no-home-access` flag to omit home access section

### Changed
- Reorganized form sections for better flow
- Improved authorization section with more comprehensive agreements

## [3.0.0] - 2026-01-20

### Added
- Service-specific templates: boarding, walking, drop-in
- Multi-pet support (1-10 pet profiles per form)
- `--service-type` and `--pets` CLI options

### Changed
- Form structure now adapts based on service type

## [2.0.0] - 2025-12-10

### Added
- 7 color themes: lavender, ocean, forest, rose, sunset, neutral, midnight
- `--theme` and `--list-themes` CLI options
- Custom color support via config file

### Changed
- Redesigned form layout with theme-aware styling

## [1.0.0] - 2025-11-01

### Added
- Initial release
- Fillable PDF form generation with ReportLab
- Pet owner information section
- Pet profile section
- Vaccinations with checkboxes
- Health and medications section
- Behavior and temperament section
- Feeding and daily care section
- Authorization and signature section
- Basic CLI with business name, contact, and output options
