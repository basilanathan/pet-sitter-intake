#!/usr/bin/env python3
"""Standalone profile test runner - works without pytest.

Generates PDFs using different configuration profiles to verify the system
works correctly across various business scenarios.

Usage:
    python scripts/run_profile_tests.py
    python scripts/run_profile_tests.py --quick    # Run subset of tests
    python scripts/run_profile_tests.py --themes   # Only theme tests
    
Output: ~/Downloads/pet_sitter_intake_tests/{timestamp}/
"""

import argparse
import os
import re
import sys
import traceback
from datetime import datetime
from pathlib import Path

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pet_sitter_intake.builder import build_form
from pet_sitter_intake.themes import THEMES


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION PROFILES
# ══════════════════════════════════════════════════════════════════════════════

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
            "sections": {"home_access": True, "vaccinations": True},
        },
        "description": "Dog walking service with ocean theme",
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
            "services": "Pet Sitting, Boarding, Dog Walking",
            "location": "Miami, FL",
            "contact": "hello@sunshinepets.com",
            "theme": "sunset",
            "service_type": "general",
            "num_pets": 3,
            "fillable": True,
        },
        "description": "Multi-pet household with 3 pets",
    },
    {
        "name": "print_only_neutral",
        "config": {
            "business_name": "Professional Pet Care LLC",
            "services": "Corporate Pet Sitting Services",
            "location": "New York, NY",
            "contact": "info@propetcare.com",
            "theme": "neutral",
            "service_type": "general",
            "num_pets": 1,
            "fillable": False,
        },
        "description": "Print-only form (non-fillable)",
    },
    {
        "name": "premium_midnight",
        "config": {
            "business_name": "Elite Pet Concierge",
            "sitter_name": "Victoria Sterling",
            "services": "Luxury Pet Sitting, VIP Boarding",
            "location": "Beverly Hills, CA",
            "contact": "victoria@elitepets.com",
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
            "services": "Beach Walks, Pet Sitting",
            "location": "San Diego, CA",
            "contact": "kai@beachbuddies.pet",
            "theme": "summer",
            "service_type": "walking",
            "num_pets": 1,
            "fillable": True,
            "sections": {"vaccinations": True},
        },
        "description": "Beach-themed walking service",
    },
    {
        "name": "bold_neon",
        "config": {
            "business_name": "Neon Nights Pet Hotel",
            "services": "24/7 Boarding, Night Dog Walking",
            "location": "Las Vegas, NV",
            "contact": "stay@neonnights.pet",
            "theme": "neon",
            "service_type": "boarding",
            "num_pets": 1,
            "fillable": True,
        },
        "description": "Bold boarding with neon theme",
    },
    {
        "name": "feminine_blush",
        "config": {
            "business_name": "Pawsh Pampering Spa",
            "sitter_name": "Sophie Chen",
            "services": "Pet Spa, Grooming, Luxury Boarding",
            "location": "Seattle, WA",
            "contact": "sophie@pawshspa.com",
            "theme": "blush",
            "service_type": "boarding",
            "num_pets": 1,
            "fillable": True,
        },
        "description": "Spa service with blush theme",
    },
    {
        "name": "corporate_deepblue",
        "config": {
            "business_name": "K9 Solutions Inc.",
            "services": "Corporate Dog Walking, Office Pet Programs",
            "location": "Boston, MA",
            "contact": "hello@k9solutions.biz",
            "theme": "deepblue",
            "service_type": "walking",
            "num_pets": 1,
            "fillable": True,
            "sections": {"home_access": True, "vaccinations": True, "health_medications": True},
        },
        "description": "Corporate walking with deepblue theme",
    },
    {
        "name": "playful_berry",
        "config": {
            "business_name": "Barks & Recreation",
            "sitter_name": "Taylor Morgan",
            "services": "Playgroups, Dog Parks, Adventure Walks",
            "location": "Nashville, TN",
            "contact": "play@barksandrec.com",
            "theme": "berry",
            "service_type": "drop_in",
            "num_pets": 2,
            "fillable": True,
        },
        "description": "Playful drop-in with berry theme",
    },
    {
        "name": "energetic_fiery",
        "config": {
            "business_name": "Fetch & Go Athletics",
            "sitter_name": "Jordan Lee",
            "services": "Agility Training, Running Buddies",
            "location": "Phoenix, AZ",
            "contact": "run@fetchandgo.com",
            "theme": "fiery",
            "service_type": "walking",
            "num_pets": 1,
            "fillable": True,
            "sections": {"vaccinations": True, "health_medications": True},
        },
        "description": "Athletic service with fiery theme",
    },
]

QUICK_PROFILES = BUSINESS_PROFILES[:5]  # First 5 for quick runs


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def slugify(text):
    """Convert text to safe filename slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '_', text)
    return text.strip('_')


def create_output_dir():
    """Create timestamped output directory."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_dir = Path.home() / "Downloads" / "pet_sitter_intake_tests" / timestamp
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def format_size(size_bytes):
    """Format file size for display."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / 1024 / 1024:.2f} MB"


# ══════════════════════════════════════════════════════════════════════════════
# TEST RUNNERS
# ══════════════════════════════════════════════════════════════════════════════

def run_profile_test(profile, output_dir, subdir="profiles"):
    """Run a single profile test and return results."""
    config = profile["config"]
    profile_name = profile["name"]
    
    # Create filename
    business_slug = slugify(config["business_name"])
    theme = config.get("theme", "lavender")
    service_type = config.get("service_type", "general")
    filename = f"{business_slug}_{theme}_{service_type}.pdf"
    
    # Output path
    out_subdir = output_dir / subdir
    out_subdir.mkdir(exist_ok=True)
    output_path = out_subdir / filename
    
    try:
        build_form(config, str(output_path))
        
        if not output_path.exists():
            return {"success": False, "error": "PDF not created", "profile": profile_name}
        
        file_size = output_path.stat().st_size
        if file_size < 1000:
            return {"success": False, "error": f"PDF too small ({file_size} bytes)", "profile": profile_name}
        
        return {
            "success": True,
            "profile": profile_name,
            "filename": filename,
            "path": str(output_path),
            "size": file_size,
            "description": profile["description"],
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "profile": profile_name,
        }


def run_theme_tests(output_dir):
    """Run tests for all themes."""
    results = []
    theme_dir = output_dir / "themes"
    theme_dir.mkdir(exist_ok=True)
    
    for theme in THEMES.keys():
        config = {
            "business_name": f"Theme Test - {theme.title()}",
            "theme": theme,
            "service_type": "general",
            "num_pets": 1,
            "fillable": True,
        }
        
        filename = f"theme_{theme}.pdf"
        output_path = theme_dir / filename
        
        try:
            build_form(config, str(output_path))
            
            if output_path.exists():
                file_size = output_path.stat().st_size
                results.append({
                    "success": True,
                    "theme": theme,
                    "filename": filename,
                    "size": file_size,
                })
            else:
                results.append({"success": False, "theme": theme, "error": "PDF not created"})
        except Exception as e:
            results.append({"success": False, "theme": theme, "error": str(e)})
    
    return results


def run_pet_count_tests(output_dir):
    """Test different numbers of pets."""
    results = []
    pet_dir = output_dir / "pet_counts"
    pet_dir.mkdir(exist_ok=True)
    
    for num_pets in [1, 2, 3, 5, 10]:
        config = {
            "business_name": f"Multi-Pet Test ({num_pets} pets)",
            "theme": "lavender",
            "service_type": "general",
            "num_pets": num_pets,
            "fillable": True,
        }
        
        filename = f"pets_{num_pets:02d}.pdf"
        output_path = pet_dir / filename
        
        try:
            build_form(config, str(output_path))
            
            if output_path.exists():
                file_size = output_path.stat().st_size
                results.append({
                    "success": True,
                    "num_pets": num_pets,
                    "filename": filename,
                    "size": file_size,
                })
            else:
                results.append({"success": False, "num_pets": num_pets, "error": "PDF not created"})
        except Exception as e:
            results.append({"success": False, "num_pets": num_pets, "error": str(e)})
    
    return results


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Run profile-based PDF generation tests")
    parser.add_argument("--quick", action="store_true", help="Run quick subset of tests")
    parser.add_argument("--themes", action="store_true", help="Only run theme tests")
    parser.add_argument("--profiles", action="store_true", help="Only run business profile tests")
    parser.add_argument("--pets", action="store_true", help="Only run pet count tests")
    args = parser.parse_args()
    
    # Create output directory
    output_dir = create_output_dir()
    print(f"\n{'=' * 60}")
    print("PET SITTER INTAKE FORM - PROFILE TESTS")
    print(f"{'=' * 60}")
    print(f"Output: {output_dir}")
    print()
    
    # Track results
    all_results = []
    passed = 0
    failed = 0
    
    # Determine which tests to run
    run_all = not (args.themes or args.profiles or args.pets)
    
    # Business profiles
    if run_all or args.profiles:
        profiles = QUICK_PROFILES if args.quick else BUSINESS_PROFILES
        print(f"Running {len(profiles)} business profile tests...")
        print("-" * 60)
        
        for profile in profiles:
            result = run_profile_test(profile, output_dir, "profiles")
            all_results.append(result)
            
            if result["success"]:
                passed += 1
                print(f"  ✅ {result['profile']}: {result['filename']} ({format_size(result['size'])})")
            else:
                failed += 1
                print(f"  ❌ {result['profile']}: {result['error']}")
        print()
    
    # Theme tests
    if run_all or args.themes:
        print(f"Running {len(THEMES)} theme tests...")
        print("-" * 60)
        
        theme_results = run_theme_tests(output_dir)
        for result in theme_results:
            all_results.append(result)
            
            if result["success"]:
                passed += 1
                print(f"  ✅ {result['theme']}: {result['filename']} ({format_size(result['size'])})")
            else:
                failed += 1
                print(f"  ❌ {result['theme']}: {result['error']}")
        print()
    
    # Pet count tests
    if run_all or args.pets:
        print("Running pet count tests...")
        print("-" * 60)
        
        pet_results = run_pet_count_tests(output_dir)
        for result in pet_results:
            all_results.append(result)
            
            if result["success"]:
                passed += 1
                print(f"  ✅ {result['num_pets']} pets: {result['filename']} ({format_size(result['size'])})")
            else:
                failed += 1
                print(f"  ❌ {result['num_pets']} pets: {result['error']}")
        print()
    
    # Generate manifest
    manifest_path = output_dir / "manifest.txt"
    with open(manifest_path, "w") as f:
        f.write(f"Pet Sitter Intake Form - Test Run\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Output directory: {output_dir}\n")
        f.write(f"{'=' * 60}\n\n")
        
        for result in all_results:
            if result.get("success"):
                label = result.get('profile') or result.get('theme') or f"{result.get('num_pets')} pets"
                f.write(f"✅ {label}\n")
                f.write(f"   File: {result.get('filename', 'N/A')}\n")
                f.write(f"   Size: {result.get('size', 0):,} bytes\n")
                if result.get("description"):
                    f.write(f"   Description: {result['description']}\n")
                f.write("\n")
            else:
                label = result.get('profile') or result.get('theme') or 'Unknown'
                f.write(f"❌ {label}\n")
                f.write(f"   Error: {result.get('error', 'Unknown error')}\n\n")
        
        f.write(f"\n{'=' * 60}\n")
        f.write(f"SUMMARY: {passed} passed, {failed} failed\n")
    
    # Count total files and size
    pdf_count = len(list(output_dir.rglob("*.pdf")))
    total_size = sum(f.stat().st_size for f in output_dir.rglob("*.pdf"))
    
    # Print summary
    print(f"{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Tests passed: {passed}")
    print(f"  Tests failed: {failed}")
    print(f"  PDFs generated: {pdf_count}")
    print(f"  Total size: {format_size(total_size)}")
    print(f"  Output: {output_dir}")
    print(f"  Manifest: {manifest_path}")
    print(f"{'=' * 60}")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
