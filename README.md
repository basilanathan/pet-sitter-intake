# Pet Sitter Client Intake Form Generator

[![ClawHub](https://img.shields.io/badge/ClawHub-pet--sitter--intake-blue)](https://clawhub.ai/skills/pet-sitter-intake)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Generate professional, branded PDF client intake forms for pet sitting businesses. Features fillable form fields, custom color themes, multi-pet support, and service-specific templates.

## Features

- **Fillable PDF Fields** — Interactive text fields and checkboxes for digital completion
- **13 Color Themes** — Match your business branding (run `--list-themes` to see all)
- **Multi-Pet Support** — Generate forms with separate profiles for 1-10 pets
- **Service Templates** — Specialized sections for boarding, dog walking, and drop-in visits
- **Home Access Section** — Key codes, alarm info, WiFi, parking instructions
- **YAML Config Files** — Save business presets for consistent form generation

## Quick Start

```bash
# Install dependencies
pip install reportlab pyyaml

# Generate a basic form
python scripts/generate_form.py \
  --business-name "Happy Paws Pet Sitting" \
  --contact "hello@happypaws.com" \
  --output client_intake_form.pdf
```

## Installation

### Via ClawHub

```bash
clawhub install pet-sitter-intake
```

### Manual Installation

```bash
git clone https://github.com/basilanathan/pet-sitter-intake.git
cd pet-sitter-intake
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python scripts/generate_form.py \
  --business-name "Pawsitive Care" \
  --sitter-name "Jane Smith" \
  --services "Dog Walking, Pet Sitting, Boarding" \
  --location "Portland, OR" \
  --contact "jane@pawsitivecare.com | (503) 555-1234"
```

### With Color Theme

```bash
python scripts/generate_form.py \
  --business-name "Ocean Breeze Pet Care" \
  --theme ocean \
  --output ocean_intake.pdf

# See all themes
python scripts/generate_form.py --list-themes
```

### Multi-Pet Form

```bash
python scripts/generate_form.py \
  --business-name "Happy Tails" \
  --pets 3 \
  --output multi_pet_form.pdf
```

### Service-Specific Templates

```bash
# Boarding (adds drop-off/pickup times, items checklist)
python scripts/generate_form.py --service-type boarding

# Dog Walking (adds leash behavior, route preferences)
python scripts/generate_form.py --service-type walking

# Drop-in Visits (adds per-visit task checklist)
python scripts/generate_form.py --service-type drop_in
```

### Using a Config File

Create `config.yaml`:

```yaml
business_name: "Happy Paws Pet Sitting"
sitter_name: "Jane Smith"
services: "Dog Walking, Boarding, Drop-in Visits"
location: "Austin, TX"
contact: "jane@happypaws.com"
theme: ocean
service_type: general
num_pets: 1
fillable: true
include_home_access: true
```

Generate:

```bash
python scripts/generate_form.py --config config.yaml
```

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--business-name` | Business name for header | "Your Business Name" |
| `--sitter-name` | Sitter name for authorization text | — |
| `--services` | Comma-separated services offered | "Pet Sitting, Dog Walking, Boarding" |
| `--location` | City/state for header | — |
| `--contact` | Contact info for footer | — |
| `--theme` | Color theme | lavender |
| `--service-type` | Form template type (sets section defaults) | general |
| `--pets` | Number of pet profile pages | 1 |
| `--fillable` | Enable fillable PDF fields | ✓ (default) |
| `--no-fillable` | Generate print-only version | — |
| `--include-section` | Include a section (repeatable) | — |
| `--exclude-section` | Exclude a section (repeatable) | — |
| `--list-sections` | Show section defaults by service type | — |
| `--config`, `-c` | Path to YAML config file | — |
| `--output`, `-o` | Output PDF path | ~/Downloads/client_intake_form.pdf |
| `--list-themes` | Show available themes | — |

## Section Configuration

Each `service_type` includes different sections by default. You can override any section.

### Section Defaults by Service Type

| Section | general | boarding | walking | drop_in |
|---------|:-------:|:--------:|:-------:|:-------:|
| `home_access` | ✓ | — | — | ✓ |
| `vaccinations` | ✓ | ✓ | — | ✓ |
| `health_medications` | ✓ | ✓ | — | ✓ |
| `feeding_daily_care` | ✓ | ✓ | — | ✓ |
| `behavior_temperament` | ✓ | ✓ | ✓ | ✓ |
| `service_specific` | — | ✓ | ✓ | ✓ |

### Override via CLI

```bash
# Walking service that needs vaccinations for group walks
python scripts/generate_form.py --service-type walking --include-section vaccinations

# General form without home access
python scripts/generate_form.py --exclude-section home_access

# Multiple overrides
python scripts/generate_form.py --service-type walking \
  --include-section vaccinations \
  --include-section health_medications
```

### Override via Config File

```yaml
service_type: walking
sections:
  vaccinations: true
  health_medications: true
  home_access: true
```

## Color Themes

| Theme | Colors | Best For |
|-------|--------|----------|
| `lavender` | Purple & peach | Friendly, approachable |
| `ocean` | Blue & sandy yellow | Calm, professional |
| `forest` | Green & gold | Natural, outdoorsy |
| `rose` | Pink & tan | Warm, nurturing |
| `sunset` | Orange & sky blue | Energetic, fun |
| `neutral` | Gray & soft blue | Corporate, clean |
| `midnight` | Slate & gold | Elegant, premium |
| `summer` | Sky blue & golden yellow | Bright, cheerful |
| `neon` | Coral & orange | Bold, modern |
| `berry` | Peachy pink & salmon | Playful, feminine |
| `fiery` | Coral & bright orange | Energetic, bold |
| `blush` | Pink gradient | Soft, gentle |
| `deepblue` | Blue gradient | Professional, trustworthy |

### Custom Colors

```yaml
theme: custom
colors:
  primary: "#YOUR_LIGHT_COLOR"
  primary_mid: "#YOUR_MID_COLOR"
  primary_dark: "#YOUR_DARK_COLOR"
  accent: "#YOUR_ACCENT"
  accent_light: "#YOUR_BG_COLOR"
  text: "#333333"
  text_muted: "#666666"
  text_light: "#999999"
```

## Form Sections

### Always Included
1. **Pet Owner Information** — Contact details, emergency contact, vet info
2. **Home Access** — Keys, codes, WiFi, parking *(can disable with `--no-home-access`)*
3. **Pet Profile** — Basic info, microchip, flea prevention
4. **Vaccinations** — Interactive checkbox table with expiration dates
5. **Health & Medications** — Allergies, conditions, medication table
6. **Behavior & Temperament** — Triggers, anxiety, escape risks, commands
7. **Feeding & Daily Care** — Food, schedule, treats, exercise
8. **Authorization & Signature** — Vet care, transport, photo release, liability

### Service-Specific Sections
- **Boarding** — Drop-off/pickup times, items to bring
- **Walking** — Leash behavior, route preferences, walk duration
- **Drop-in** — Per-visit task checklist (feed, water, potty, meds, etc.)

## Requirements

- Python 3.8 or higher
- reportlab >= 4.0.0
- pyyaml >= 6.0 (optional, for config files)

## Development

### Running Tests

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

### Config Validation

The generator validates configuration values and auto-corrects invalid inputs:
- `num_pets` is clamped to 1-10
- Invalid `service_type` falls back to "general"
- Invalid `theme` falls back to "lavender"
- Warnings are printed for any corrections made

## Examples

See the `examples/` folder for sample config files:
- `examples/boarding_business.yaml` — Overnight boarding facility
- `examples/dog_walker.yaml` — Dog walking service
- `examples/in_home_sitter.yaml` — In-home pet sitting

## License

MIT License — See [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## Permissions

This skill requires the following permissions when used via ClawHub:

| Permission | Justification |
|------------|---------------|
| `filesystem` | Write generated PDF files to the user's specified output path |
| `shell` | Execute the Python script (`python scripts/generate_form.py`) |

No network access is required. All processing happens locally.

## Troubleshooting

### "reportlab not found"
Install dependencies: `pip install reportlab pyyaml`

### PDF not fillable
Ensure you're not using `--no-fillable`. Fillable fields are enabled by default.

### Form looks different than expected
Check your theme with `--list-themes`. Default is `lavender`.

### Config file not loading
Verify YAML syntax. Use the examples in `examples/` as a reference.

### Permission denied on output
Ensure you have write access to the output directory.

## Support

- **Issues**: [GitHub Issues](https://github.com/basilanathan/pet-sitter-intake/issues)
- **ClawHub**: [Skill Page](https://clawhub.ai/skills/pet-sitter-intake)
