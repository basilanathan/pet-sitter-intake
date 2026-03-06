"""Page builders for intake form PDF generation.

This subpackage contains modular page builders that each handle
a specific section of the intake form. The main builder.py orchestrates
these page builders using FormContext.

Usage:
    from .pages import FormContext, build_owner_info_page, build_authorization_page
    
    ctx = FormContext.from_config(config)
    story = []
    story += build_owner_info_page(ctx)
    story += build_home_access_page(ctx)
    # ... etc
"""

from .context import FormContext

from .owner_info import (
    build_hero_section,
    build_owner_info_section,
    build_communication_prefs,
    build_owner_info_page,
)

from .home_access import (
    build_home_access_section,
    build_home_access_page,
)

from .pet_profile import (
    build_pet_basic_info,
    build_vaccinations_section,
    build_health_medications_section,
    build_feeding_section,
    build_pet_profile_page1,
    build_pet_profile_page2,
    build_all_pet_profiles,
)

from .service_specific import (
    build_walking_section,
    build_boarding_section,
    build_dropin_section,
    build_service_specific_page,
)

from .authorization import (
    build_authorization_blocks,
    build_permission_checkboxes,
    build_signature_block,
    build_office_use_block,
    build_page_footer,
    build_authorization_page,
)

__all__ = [
    # Context
    "FormContext",
    
    # Owner info (page 1)
    "build_hero_section",
    "build_owner_info_section",
    "build_communication_prefs",
    "build_owner_info_page",
    
    # Home access (optional page)
    "build_home_access_section",
    "build_home_access_page",
    
    # Pet profile (1-2 pages per pet)
    "build_pet_basic_info",
    "build_vaccinations_section",
    "build_health_medications_section",
    "build_feeding_section",
    "build_pet_profile_page1",
    "build_pet_profile_page2",
    "build_all_pet_profiles",
    
    # Service specific (optional page)
    "build_walking_section",
    "build_boarding_section",
    "build_dropin_section",
    "build_service_specific_page",
    
    # Authorization (last page)
    "build_authorization_blocks",
    "build_permission_checkboxes",
    "build_signature_block",
    "build_office_use_block",
    "build_page_footer",
    "build_authorization_page",
]
