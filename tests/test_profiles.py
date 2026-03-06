"""Profile-based integration tests for PDF generation.

These tests generate actual PDFs using different configuration profiles
to verify the system works correctly across various business scenarios.

Output directory: ~/Downloads/pet_sitter_intake_tests/{run_id}/
Run ID format: YYYY-MM-DD_HH-MM-SS

Run with: pytest tests/test_profiles.py -v
"""

import os
import re
from datetime import datetime
from pathlib import Path

import pytest

from pet_sitter_intake.builder import build_form
from pet_sitter_intake.themes import THEMES


# ══════════════════════════════════════════════════════════════════════════════
# TEST OUTPUT DIRECTORY SETUP
# ══════════════════════════════════════════════════════════════════════════════

def get_test_output_dir():
    """Get or create the test output directory for this test run.
    
    Returns path like: ~/Downloads/pet_sitter_intake_tests/2026-03-05_14-30-00/
    """
    base_dir = Path.home() / "Downloads" / "pet_sitter_intake_tests"
    
    # Use a module-level timestamp so all tests in one run share the same dir
    if not hasattr(get_test_output_dir, "_run_id"):
        get_test_output_dir._run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    run_dir = base_dir / get_test_output_dir._run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    
    return run_dir


def slugify(text):
    """Convert text to a safe filename slug.
    
    Example: "Happy Paws Pet Sitting!" -> "happy_paws_pet_sitting"
    """
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '_', text)
    return text.strip('_')


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION PROFILES
# ══════════════════════════════════════════════════════════════════════════════

# Each profile represents a realistic business configuration
# Easy to add new profiles by adding to this list

BUSINESS_PROFILES = [
    {
        "name": "basic_lavender",
        "config": {
            "business_name": "Happy Paws Pet Sitting",
            "sitter_name": "Jane Smith",
            "services": "Pet Sitting, Dog Walking",
            "location": "Portland, OR",
            "contact": "jane@happypaws.com | (503) 555-1234",
            "theme": "lavender",
            "service_type": "general",
            "num_pets": 1,
            "fillable": True,
        },
        "description": "Basic general form with lavender theme",
    },
    {
        "name": "boarding_forest",
        "config": {
            "business_name": "Cozy Canine Boarding",
            "sitter_name": "",
            "services": "Overnight Boarding, Doggy Daycare, Grooming",
            "location": "Denver, CO",
            "contact": "(303) 555-7890 | stay@cozycanine.com",
            "theme": "forest",
            "service_type": "boarding",
            "num_pets": 1,
            "fillable": True,
        },
        "description": "Boarding facility with forest theme",
    },
    {
        "name": "walking_ocean",
        "config": {
            "business_name": "Urban Paws Dog Walking",
            "sitter_name": "Alex Rivera",
            "services": "Dog Walking, Potty Breaks, Park Visits",
            "location": "Chicago, IL",
            "contact": "alex@urbanpaws.dog | (312) 555-WALK",
            "theme": "ocean",
            "service_type": "walking",
            "num_pets": 1,
            "fillable": True,
            "sections": {
                "home_access": True,
                "vaccinations": True,
            },
        },
        "description": "Dog walking service with ocean theme and extra sections",
    },
    {
        "name": "drop_in_rose",
        "config": {
            "business_name": "Tender Loving Care Pet Services",
            "sitter_name": "Maria Garcia",
            "services": "Drop-in Visits, Pet Sitting, House Sitting",
            "location": "Austin, TX",
            "contact": "maria@tlcpets.com | (512) 555-PETS",
            "theme": "rose",
            "service_type": "drop_in",
            "num_pets": 2,
            "fillable": True,
        },
        "description": "Drop-in service with rose theme and 2 pets",
    },
    {
        "name": "multi_pet_sunset",
        "config": {
            "business_name": "Sunshine Pet Paradise",
            "sitter_name": "Chris Johnson",
            "services": "Pet Sitting, Boarding, Dog Walking, Drop-in Visits",
            "location": "Miami, FL",
            "contact": "hello@sunshinepets.com | (305) 555-SUN1",
            "theme": "sunset",
            "service_type": "general",
            "num_pets": 3,
            "fillable": True,
        },
        "description": "Multi-pet household with 3 pets and sunset theme",
    },
    {
        "name": "print_only_neutral",
        "config": {
            "business_name": "Professional Pet Care LLC",
            "sitter_name": "",
            "services": "Corporate Pet Sitting Services",
            "location": "New York, NY",
            "contact": "info@propetcare.com | (212) 555-0000",
            "theme": "neutral",
            "service_type": "general",
            "num_pets": 1,
            "fillable": False,
        },
        "description": "Print-only form (non-fillable) with neutral theme",
    },
    {
        "name": "premium_midnight",
        "config": {
            "business_name": "Elite Pet Concierge",
            "sitter_name": "Victoria Sterling",
            "services": "Luxury Pet Sitting, VIP Boarding, Personal Pet Assistant",
            "location": "Beverly Hills, CA",
            "contact": "victoria@elitepets.com | (310) 555-LUXE",
            "theme": "midnight",
            "service_type": "boarding",
            "num_pets": 2,
            "fillable": True,
        },
        "description": "Premium boarding with midnight theme",
    },
    {
        "name": "summer_vibes",
        "config": {
            "business_name": "Beach Buddies Pet Care",
            "sitter_name": "Kai Nakamura",
            "services": "Beach Walks, Pet Sitting, Surf Dog Training",
            "location": "San Diego, CA",
            "contact": "kai@beachbuddies.pet | (619) 555-SURF",
            "theme": "summer",
            "service_type": "walking",
            "num_pets": 1,
            "fillable": True,
            "sections": {
                "vaccinations": True,
            },
        },
        "description": "Beach-themed walking service with summer theme",
    },
    {
        "name": "bold_neon",
        "config": {
            "business_name": "Neon Nights Pet Hotel",
            "sitter_name": "",
            "services": "24/7 Boarding, Night Owl Dog Walking",
            "location": "Las Vegas, NV",
            "contact": "stay@neonnights.pet | (702) 555-NEON",
            "theme": "neon",
            "service_type": "boarding",
            "num_pets": 1,
            "fillable": True,
        },
        "description": "Bold boarding facility with neon theme",
    },
    {
        "name": "feminine_blush",
        "config": {
            "business_name": "Pawsh Pampering Spa",
            "sitter_name": "Sophie Chen",
            "services": "Pet Spa, Grooming, Luxury Boarding",
            "location": "Seattle, WA",
            "contact": "sophie@pawshspa.com | (206) 555-PAWSH",
            "theme": "blush",
            "service_type": "boarding",
            "num_pets": 1,
            "fillable": True,
        },
        "description": "Spa/grooming service with blush theme",
    },
    {
        "name": "corporate_deepblue",
        "config": {
            "business_name": "K9 Solutions Inc.",
            "sitter_name": "",
            "services": "Corporate Dog Walking, Office Pet Programs",
            "location": "Boston, MA",
            "contact": "hello@k9solutions.biz | (617) 555-K9K9",
            "theme": "deepblue",
            "service_type": "walking",
            "num_pets": 1,
            "fillable": True,
            "sections": {
                "home_access": True,
                "vaccinations": True,
                "health_medications": True,
            },
        },
        "description": "Corporate walking service with deepblue theme",
    },
    {
        "name": "playful_berry",
        "config": {
            "business_name": "Barks & Recreation",
            "sitter_name": "Taylor Morgan",
            "services": "Playgroups, Dog Parks, Adventure Walks",
            "location": "Nashville, TN",
            "contact": "play@barksandrec.com | (615) 555-BARK",
            "theme": "berry",
            "service_type": "drop_in",
            "num_pets": 2,
            "fillable": True,
        },
        "description": "Playful drop-in service with berry theme",
    },
    {
        "name": "energetic_fiery",
        "config": {
            "business_name": "Fetch & Go Athletics",
            "sitter_name": "Jordan Lee",
            "services": "Agility Training, Running Buddies, Active Dog Care",
            "location": "Phoenix, AZ",
            "contact": "run@fetchandgo.com | (480) 555-RUN1",
            "theme": "fiery",
            "service_type": "walking",
            "num_pets": 1,
            "fillable": True,
            "sections": {
                "vaccinations": True,
                "health_medications": True,
            },
        },
        "description": "Athletic dog service with fiery theme",
    },
]

# Theme-specific tests to ensure all themes render correctly
THEME_TEST_PROFILES = [
    {
        "name": f"theme_test_{theme}",
        "config": {
            "business_name": f"Theme Test - {theme.title()}",
            "sitter_name": "Test Sitter",
            "services": "Theme Testing Service",
            "location": "Test City, TS",
            "contact": f"test@{theme}.example.com",
            "theme": theme,
            "service_type": "general",
            "num_pets": 1,
            "fillable": True,
        },
        "description": f"Theme validation test for {theme}",
    }
    for theme in THEMES.keys()
]

# Service type tests with minimal sections
SERVICE_TYPE_PROFILES = [
    {
        "name": "service_general_full",
        "config": {
            "business_name": "General Service Test",
            "theme": "lavender",
            "service_type": "general",
            "num_pets": 1,
            "fillable": True,
        },
        "description": "General service type with all default sections",
    },
    {
        "name": "service_boarding_minimal",
        "config": {
            "business_name": "Boarding Service Test",
            "theme": "forest",
            "service_type": "boarding",
            "num_pets": 1,
            "fillable": True,
        },
        "description": "Boarding service type with default sections",
    },
    {
        "name": "service_walking_minimal",
        "config": {
            "business_name": "Walking Service Test",
            "theme": "ocean",
            "service_type": "walking",
            "num_pets": 1,
            "fillable": True,
        },
        "description": "Walking service type (minimal sections)",
    },
    {
        "name": "service_dropin_full",
        "config": {
            "business_name": "Drop-in Service Test",
            "theme": "rose",
            "service_type": "drop_in",
            "num_pets": 1,
            "fillable": True,
        },
        "description": "Drop-in service type with all sections",
    },
]

# Custom color tests
CUSTOM_COLOR_PROFILES = [
    {
        "name": "custom_brand_red",
        "config": {
            "business_name": "Red Brand Test",
            "theme": "custom",
            "colors": {
                "primary": "#FFE0E0",
                "primary_mid": "#FF6B6B",
                "primary_dark": "#C92A2A",
                "accent": "#FFD93D",
                "accent_light": "#FFF5E6",
            },
            "service_type": "general",
            "num_pets": 1,
            "fillable": True,
        },
        "description": "Custom red/yellow brand colors",
    },
    {
        "name": "custom_brand_teal",
        "config": {
            "business_name": "Teal Brand Test",
            "theme": "custom",
            "colors": {
                "primary": "#E0F7FA",
                "primary_mid": "#4DB6AC",
                "primary_dark": "#00796B",
                "accent": "#FFB74D",
                "accent_light": "#FFF8E1",
            },
            "service_type": "boarding",
            "num_pets": 1,
            "fillable": True,
        },
        "description": "Custom teal/orange brand colors",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# TEST FIXTURES
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="module")
def output_dir():
    """Fixture providing the test output directory."""
    return get_test_output_dir()


@pytest.fixture(scope="module")
def manifest_file(output_dir):
    """Create a manifest file listing all generated PDFs."""
    manifest_path = output_dir / "manifest.txt"
    with open(manifest_path, "w") as f:
        f.write(f"Pet Sitter Intake Form - Test Run\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Output directory: {output_dir}\n")
        f.write("=" * 60 + "\n\n")
    return manifest_path


def append_to_manifest(manifest_path, profile_name, filename, description, file_size):
    """Append a test result to the manifest file."""
    with open(manifest_path, "a") as f:
        f.write(f"Profile: {profile_name}\n")
        f.write(f"  File: {filename}\n")
        f.write(f"  Size: {file_size:,} bytes\n")
        f.write(f"  Description: {description}\n\n")


# ══════════════════════════════════════════════════════════════════════════════
# TEST CLASSES
# ══════════════════════════════════════════════════════════════════════════════

class TestBusinessProfiles:
    """Test PDF generation for various business profiles."""
    
    @pytest.mark.parametrize("profile", BUSINESS_PROFILES, ids=lambda p: p["name"])
    def test_business_profile(self, profile, output_dir, manifest_file):
        """Generate PDF for a business profile and verify it was created."""
        config = profile["config"]
        profile_name = profile["name"]
        description = profile["description"]
        
        # Create filename from business name
        business_slug = slugify(config["business_name"])
        theme = config.get("theme", "lavender")
        service_type = config.get("service_type", "general")
        filename = f"{business_slug}_{theme}_{service_type}.pdf"
        output_path = output_dir / filename
        
        # Generate the PDF
        build_form(config, str(output_path))
        
        # Verify PDF was created
        assert output_path.exists(), f"PDF not created: {output_path}"
        
        # Verify file has content
        file_size = output_path.stat().st_size
        assert file_size > 1000, f"PDF too small ({file_size} bytes), likely corrupted"
        
        # Append to manifest
        append_to_manifest(manifest_file, profile_name, filename, description, file_size)
        
        # Return info for potential further verification
        return {
            "path": output_path,
            "size": file_size,
            "config": config,
        }


class TestThemeCoverage:
    """Ensure all themes generate valid PDFs."""
    
    @pytest.mark.parametrize("profile", THEME_TEST_PROFILES, ids=lambda p: p["name"])
    def test_theme(self, profile, output_dir, manifest_file):
        """Generate PDF for each theme and verify colors are applied."""
        config = profile["config"]
        profile_name = profile["name"]
        description = profile["description"]
        theme = config["theme"]
        
        filename = f"theme_{theme}.pdf"
        output_path = output_dir / "themes" / filename
        output_path.parent.mkdir(exist_ok=True)
        
        # Generate the PDF
        build_form(config, str(output_path))
        
        # Verify PDF was created
        assert output_path.exists(), f"PDF not created for theme {theme}"
        
        file_size = output_path.stat().st_size
        assert file_size > 1000, f"Theme {theme} PDF too small"
        
        append_to_manifest(manifest_file, profile_name, f"themes/{filename}", description, file_size)


class TestServiceTypes:
    """Test all service types generate correctly."""
    
    @pytest.mark.parametrize("profile", SERVICE_TYPE_PROFILES, ids=lambda p: p["name"])
    def test_service_type(self, profile, output_dir, manifest_file):
        """Generate PDF for each service type and verify sections."""
        config = profile["config"]
        profile_name = profile["name"]
        description = profile["description"]
        service_type = config["service_type"]
        
        filename = f"service_{service_type}.pdf"
        output_path = output_dir / "service_types" / filename
        output_path.parent.mkdir(exist_ok=True)
        
        # Generate the PDF
        build_form(config, str(output_path))
        
        # Verify PDF was created
        assert output_path.exists(), f"PDF not created for service type {service_type}"
        
        file_size = output_path.stat().st_size
        assert file_size > 1000, f"Service type {service_type} PDF too small"
        
        # Walking forms should be smaller (fewer sections)
        if service_type == "walking":
            assert file_size < 100000, "Walking form unexpectedly large"
        
        append_to_manifest(manifest_file, profile_name, f"service_types/{filename}", description, file_size)


class TestCustomColors:
    """Test custom color configurations."""
    
    @pytest.mark.parametrize("profile", CUSTOM_COLOR_PROFILES, ids=lambda p: p["name"])
    def test_custom_colors(self, profile, output_dir, manifest_file):
        """Generate PDF with custom brand colors."""
        config = profile["config"]
        profile_name = profile["name"]
        description = profile["description"]
        
        business_slug = slugify(config["business_name"])
        filename = f"custom_{business_slug}.pdf"
        output_path = output_dir / "custom_colors" / filename
        output_path.parent.mkdir(exist_ok=True)
        
        # Generate the PDF
        build_form(config, str(output_path))
        
        # Verify PDF was created
        assert output_path.exists(), f"PDF not created for custom colors"
        
        file_size = output_path.stat().st_size
        assert file_size > 1000, f"Custom color PDF too small"
        
        append_to_manifest(manifest_file, profile_name, f"custom_colors/{filename}", description, file_size)


class TestMultiPetVariations:
    """Test different numbers of pets."""
    
    @pytest.mark.parametrize("num_pets", [1, 2, 3, 5, 10])
    def test_pet_count(self, num_pets, output_dir, manifest_file):
        """Generate PDFs with varying numbers of pets."""
        config = {
            "business_name": f"Multi-Pet Test ({num_pets} pets)",
            "theme": "lavender",
            "service_type": "general",
            "num_pets": num_pets,
            "fillable": True,
        }
        
        filename = f"pets_{num_pets:02d}.pdf"
        output_path = output_dir / "pet_counts" / filename
        output_path.parent.mkdir(exist_ok=True)
        
        # Generate the PDF
        build_form(config, str(output_path))
        
        # Verify PDF was created
        assert output_path.exists(), f"PDF not created for {num_pets} pets"
        
        file_size = output_path.stat().st_size
        
        # More pets = larger file
        min_size = 5000 + (num_pets * 10000)
        assert file_size > min_size, f"PDF for {num_pets} pets seems too small"
        
        append_to_manifest(
            manifest_file, 
            f"pet_count_{num_pets}", 
            f"pet_counts/{filename}", 
            f"Form with {num_pets} pet profile(s)",
            file_size
        )


class TestFillableVariations:
    """Test fillable vs non-fillable forms."""
    
    @pytest.mark.parametrize("fillable", [True, False], ids=["fillable", "print_only"])
    def test_fillable_mode(self, fillable, output_dir, manifest_file):
        """Generate both fillable and print-only versions."""
        mode = "fillable" if fillable else "print_only"
        config = {
            "business_name": f"Fillable Test ({mode})",
            "theme": "neutral",
            "service_type": "general",
            "num_pets": 1,
            "fillable": fillable,
        }
        
        filename = f"form_{mode}.pdf"
        output_path = output_dir / "fillable_modes" / filename
        output_path.parent.mkdir(exist_ok=True)
        
        # Generate the PDF
        build_form(config, str(output_path))
        
        # Verify PDF was created
        assert output_path.exists(), f"PDF not created for {mode} mode"
        
        file_size = output_path.stat().st_size
        
        append_to_manifest(
            manifest_file,
            f"fillable_{mode}",
            f"fillable_modes/{filename}",
            f"Form in {mode} mode",
            file_size
        )


class TestSectionCombinations:
    """Test various section include/exclude combinations."""
    
    def test_minimal_sections(self, output_dir, manifest_file):
        """Generate form with minimal sections enabled."""
        config = {
            "business_name": "Minimal Sections Test",
            "theme": "neutral",
            "service_type": "general",
            "num_pets": 1,
            "fillable": True,
            "sections": {
                "home_access": False,
                "vaccinations": False,
                "health_medications": False,
                "feeding_daily_care": False,
                "behavior_temperament": True,
                "service_specific": False,
            },
        }
        
        filename = "sections_minimal.pdf"
        output_path = output_dir / "section_combos" / filename
        output_path.parent.mkdir(exist_ok=True)
        
        build_form(config, str(output_path))
        
        assert output_path.exists()
        file_size = output_path.stat().st_size
        
        # Minimal should be smaller
        assert file_size < 50000, "Minimal form unexpectedly large"
        
        append_to_manifest(
            manifest_file,
            "sections_minimal",
            f"section_combos/{filename}",
            "Form with only behavior section",
            file_size
        )
    
    def test_all_sections(self, output_dir, manifest_file):
        """Generate form with all sections enabled."""
        config = {
            "business_name": "All Sections Test",
            "theme": "neutral",
            "service_type": "drop_in",  # Drop-in has most sections by default
            "num_pets": 1,
            "fillable": True,
            "sections": {
                "home_access": True,
                "vaccinations": True,
                "health_medications": True,
                "feeding_daily_care": True,
                "behavior_temperament": True,
                "service_specific": True,
            },
        }
        
        filename = "sections_all.pdf"
        output_path = output_dir / "section_combos" / filename
        output_path.parent.mkdir(exist_ok=True)
        
        build_form(config, str(output_path))
        
        assert output_path.exists()
        file_size = output_path.stat().st_size
        
        append_to_manifest(
            manifest_file,
            "sections_all",
            f"section_combos/{filename}",
            "Form with all sections enabled",
            file_size
        )


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_long_business_name(self, output_dir, manifest_file):
        """Test with a very long business name."""
        config = {
            "business_name": "The Absolutely Wonderful Amazing Fantastic Super Duper Pet Sitting and Dog Walking Service Company LLC",
            "theme": "lavender",
            "service_type": "general",
            "num_pets": 1,
            "fillable": True,
        }
        
        filename = "edge_long_name.pdf"
        output_path = output_dir / "edge_cases" / filename
        output_path.parent.mkdir(exist_ok=True)
        
        build_form(config, str(output_path))
        
        assert output_path.exists()
        file_size = output_path.stat().st_size
        
        append_to_manifest(
            manifest_file,
            "edge_long_name",
            f"edge_cases/{filename}",
            "Very long business name",
            file_size
        )
    
    def test_special_characters_in_name(self, output_dir, manifest_file):
        """Test with special characters in business name."""
        config = {
            "business_name": "Paws & Claws Pet Care — \"The Best!\"",
            "sitter_name": "José García",
            "location": "San José, CA",
            "contact": "josé@pawsandclaws.com",
            "theme": "rose",
            "service_type": "general",
            "num_pets": 1,
            "fillable": True,
        }
        
        filename = "edge_special_chars.pdf"
        output_path = output_dir / "edge_cases" / filename
        output_path.parent.mkdir(exist_ok=True)
        
        build_form(config, str(output_path))
        
        assert output_path.exists()
        file_size = output_path.stat().st_size
        
        append_to_manifest(
            manifest_file,
            "edge_special_chars",
            f"edge_cases/{filename}",
            "Special characters and accents",
            file_size
        )
    
    def test_empty_optional_fields(self, output_dir, manifest_file):
        """Test with minimal required fields only."""
        config = {
            "business_name": "Minimal Fields Test",
            "theme": "neutral",
        }
        
        filename = "edge_minimal_config.pdf"
        output_path = output_dir / "edge_cases" / filename
        output_path.parent.mkdir(exist_ok=True)
        
        build_form(config, str(output_path))
        
        assert output_path.exists()
        file_size = output_path.stat().st_size
        
        append_to_manifest(
            manifest_file,
            "edge_minimal_config",
            f"edge_cases/{filename}",
            "Only required config fields",
            file_size
        )


# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY FIXTURE
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="module", autouse=True)
def test_summary(output_dir, manifest_file, request):
    """Print summary after all tests complete."""
    yield
    
    # Count PDFs generated
    pdf_count = len(list(output_dir.rglob("*.pdf")))
    total_size = sum(f.stat().st_size for f in output_dir.rglob("*.pdf"))
    
    # Append summary to manifest
    with open(manifest_file, "a") as f:
        f.write("\n" + "=" * 60 + "\n")
        f.write("SUMMARY\n")
        f.write("=" * 60 + "\n")
        f.write(f"Total PDFs generated: {pdf_count}\n")
        f.write(f"Total size: {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)\n")
        f.write(f"Output directory: {output_dir}\n")
    
    print(f"\n{'=' * 60}")
    print(f"TEST RUN COMPLETE")
    print(f"{'=' * 60}")
    print(f"PDFs generated: {pdf_count}")
    print(f"Total size: {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)")
    print(f"Output: {output_dir}")
    print(f"Manifest: {manifest_file}")
    print(f"{'=' * 60}")
