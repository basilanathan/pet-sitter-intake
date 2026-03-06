"""PDF form builder - main form orchestrator."""

import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)

from .constants import (
    PAGE_W, WHITE, MARGINS,
    VAX_COLUMNS, MED_COLUMNS, ADDRESS_COLUMNS, PET_PROFILE_COLUMNS,
)
from .config import DEFAULT_CONFIG, get_section_config
from .themes import get_theme_colors
from .flowables import (
    CheckboxRow, FillableTextField, FillableCheckboxRow, VaxCheckboxRow,
    get_color,
)
from .layout import (
    sty, sp, hr, sec_hdr, para_row, field, two_col, three_col, pg_hdr, auth_block,
)
from .sections import (
    build_home_access_section, build_pet_behavior_section,
    build_potty_section, build_sleep_crate_section, build_service_specific_section,
)


def build_form(config, output_path):
    """Build the intake form PDF from config dict.
    
    Args:
        config: Dict with business info, theme, service_type, etc.
        output_path: Path to save the generated PDF
    """
    output_path = os.path.expanduser(output_path)
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"📁 Created directory: {output_dir}")

    theme_colors = get_theme_colors(config)
    
    business_name = config.get("business_name", DEFAULT_CONFIG["business_name"])
    sitter_name = config.get("sitter_name", DEFAULT_CONFIG["sitter_name"])
    services = config.get("services", DEFAULT_CONFIG["services"])
    location = config.get("location", DEFAULT_CONFIG["location"])
    contact = config.get("contact", DEFAULT_CONFIG["contact"])
    service_type = config.get("service_type", DEFAULT_CONFIG["service_type"])
    num_pets = config.get("num_pets", DEFAULT_CONFIG["num_pets"])
    fillable = config.get("fillable", DEFAULT_CONFIG["fillable"])
    
    sections = get_section_config(config)
    
    s = sty(theme_colors)
    doc = SimpleDocTemplate(
        output_path, 
        pagesize=letter,
        leftMargin=MARGINS["left"], 
        rightMargin=MARGINS["right"],
        topMargin=MARGINS["top"], 
        bottomMargin=MARGINS["bottom"]
    )
    story = []

    # Calculate total pages
    base_pages = 1
    if sections["home_access"]:
        base_pages += 1
    
    pet_page_2_sections = ["health_medications", "behavior_temperament", "feeding_daily_care"]
    pages_per_pet = 1
    if any(sections.get(sec, True) for sec in pet_page_2_sections):
        pages_per_pet = 2
    
    base_pages += pages_per_pet * num_pets
    
    if sections["service_specific"] and service_type != "general":
        base_pages += 1
    
    base_pages += 1
    total_pages = base_pages

    # ══════════════════════════════════════════════════════════════════════
    # PAGE 1 — PET OWNER INFORMATION
    # ══════════════════════════════════════════════════════════════════════
    hero_rows = [
        [Paragraph(business_name, s["title"])],
        [Paragraph("Client &amp; Pet Intake Form", s["subtitle"])],
        [Paragraph(f"{location}  \u00b7  {contact}", s["contact"])],
        [Paragraph(f"<b>Services:</b>  {services}", s["svc"])],
    ]
    hero = Table(hero_rows, colWidths=[PAGE_W])
    hero.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), get_color(theme_colors, "accent_light")),
        ("TOPPADDING",    (0,0),(-1,0),  18),
        ("TOPPADDING",    (0,1),(-1,-1), 3),
        ("BOTTOMPADDING", (0,-1),(-1,-1), 16),
        ("BOTTOMPADDING", (0,0),(-1,-2), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
    ]))
    story += [hero, sp(0.22)]

    story += [sec_hdr("SECTION 1  —  PET OWNER INFORMATION", s, theme_colors=theme_colors), sp(0.25)]

    story += field("Owner Full Name", s, extra_space=26, fillable=fillable, field_name="owner_name", theme_colors=theme_colors)
    story.append(two_col("Home Phone", "Cell Phone", s, fillable=fillable, 
                         field_names=["home_phone", "cell_phone"], theme_colors=theme_colors))
    story += field("Email Address", s, extra_space=26, fillable=fillable, field_name="email", theme_colors=theme_colors)
    story.append(sp(0.08))
    story += field("Street Address", s, extra_space=26, fillable=fillable, field_name="street_address", multiline=True, theme_colors=theme_colors)
    story.append(three_col(
        ["City", "State / Province", "Zip / Postal Code"], s,
        widths=[ADDRESS_COLUMNS["city"], ADDRESS_COLUMNS["state"], ADDRESS_COLUMNS["zip"]],
        fillable=fillable,
        field_names=["city", "state_province", "zip_postal"],
        theme_colors=theme_colors
    ))
    story.append(sp(0.3))

    story.append(para_row("Emergency Contact  <i>(someone other than you)</i>", s["sublbl"]))
    story.append(sp(0.1))
    story.append(two_col("Emergency Contact Name", "Relationship", s, fillable=fillable,
                         field_names=["emergency_name", "emergency_relationship"], theme_colors=theme_colors))
    story.append(two_col("Phone", "Alt Phone", s, fillable=fillable,
                         field_names=["emergency_phone", "emergency_alt_phone"], theme_colors=theme_colors))
    story.append(sp(0.3))

    story.append(para_row("Veterinarian Information", s["sublbl"]))
    story.append(sp(0.1))
    story.append(two_col("Veterinary Clinic Name", "Clinic Phone", s, fillable=fillable,
                         field_names=["vet_clinic", "vet_phone"], theme_colors=theme_colors))
    story += field("Clinic Address", s, extra_space=26, fillable=fillable, field_name="vet_address", multiline=True, theme_colors=theme_colors)
    story.append(sp(0.15))
    
    story.append(para_row("24-Hour Emergency Vet  <i>(if different from above)</i>", s["sublbl"]))
    story.append(sp(0.1))
    story.append(two_col("Emergency Vet Name", "Emergency Vet Phone", s, fillable=fillable,
                         field_names=["emergency_vet_name", "emergency_vet_phone"], theme_colors=theme_colors))
    story.append(sp(0.2))

    story += field("Person(s) Authorized to Pick Up My Pet", s, extra_space=26, fillable=fillable,
                   field_name="authorized_pickup", theme_colors=theme_colors)
    
    story.append(sp(0.15))
    story.append(para_row("Communication Preferences", s["sublbl"]))
    story.append(sp(0.1))
    story.append(para_row("How often would you like updates?", s["lbl"]))
    if fillable:
        story.append(FillableCheckboxRow("update_frequency",
            ["Daily", "Twice daily", "Only if needed", "Other"],
            per_row=4, theme_colors=theme_colors
        ))
    else:
        story.append(CheckboxRow(
            ["Daily", "Twice daily", "Only if needed", "Other"],
            per_row=4, theme_colors=theme_colors
        ))
    story.append(para_row("Preferred contact method:", s["lbl"]))
    if fillable:
        story.append(FillableCheckboxRow("contact_method",
            ["Text", "Email", "Phone call", "App (specify below)"],
            per_row=4, theme_colors=theme_colors
        ))
    else:
        story.append(CheckboxRow(
            ["Text", "Email", "Phone call", "App (specify below)"],
            per_row=4, theme_colors=theme_colors
        ))

    # ══════════════════════════════════════════════════════════════════════
    # HOME ACCESS SECTION (if enabled)
    # ══════════════════════════════════════════════════════════════════════
    current_page = 1
    if sections["home_access"]:
        story.append(PageBreak())
        current_page += 1
        story += pg_hdr(business_name, f"Page {current_page} of {total_pages}", s, theme_colors=theme_colors)
        story += build_home_access_section(s, fillable=fillable, theme_colors=theme_colors)

    # ══════════════════════════════════════════════════════════════════════
    # PET PROFILE PAGES (one set per pet)
    # ══════════════════════════════════════════════════════════════════════
    for pet_num in range(1, num_pets + 1):
        prefix = f"pet{pet_num}_" if num_pets > 1 else ""
        pet_label = f" #{pet_num}" if num_pets > 1 else ""
        
        story.append(PageBreak())
        current_page += 1
        story += pg_hdr(business_name, f"Page {current_page} of {total_pages}", s, theme_colors=theme_colors)
        story += [sec_hdr(f"PET PROFILE{pet_label}", s, theme_colors=theme_colors), sp(0.2)]
        
        if num_pets > 1:
            story.append(para_row(f"<b>Pet {pet_num} of {num_pets}</b>", s["note"]))
        
        story.append(two_col("Pet Name", "Species  (Dog / Cat / Other)", s, fillable=fillable,
                             field_names=[f"{prefix}name", f"{prefix}species"], theme_colors=theme_colors))
        story.append(two_col("Breed", "Mix?   Yes  /  No", s, fillable=fillable,
                             field_names=[f"{prefix}breed", f"{prefix}mix"], theme_colors=theme_colors))
        story.append(three_col(
            ["Age", "Weight (lbs)", "Color / Markings"], s,
            widths=[PET_PROFILE_COLUMNS["age"], PET_PROFILE_COLUMNS["weight"], PET_PROFILE_COLUMNS["color"]],
            fillable=fillable,
            field_names=[f"{prefix}age", f"{prefix}weight", f"{prefix}color_markings"],
            theme_colors=theme_colors
        ))

        story.append(para_row("Sex:", s["lbl"]))
        if fillable:
            story.append(FillableCheckboxRow(f"{prefix}sex",
                ["Male (intact)", "Male (neutered)", "Female (intact)", "Female (spayed)"],
                per_row=4, theme_colors=theme_colors
            ))
        else:
            story.append(CheckboxRow(
                ["Male (intact)", "Male (neutered)", "Female (intact)", "Female (spayed)"],
                per_row=4, theme_colors=theme_colors
            ))
        story.append(sp(0.12))
        story.append(two_col("Microchip #", "License / Tag #", s, fillable=fillable,
                             field_names=[f"{prefix}microchip", f"{prefix}license"], theme_colors=theme_colors))
        story.append(sp(0.15))
        
        story.append(para_row("Flea/Tick Prevention", s["sublbl"]))
        story.append(sp(0.1))
        story.append(two_col("Prevention product used", "Last applied date", s, fillable=fillable,
                             field_names=[f"{prefix}flea_product", f"{prefix}flea_date"], theme_colors=theme_colors))
        story.append(sp(0.15))

        if sections["vaccinations"]:
            story += [sec_hdr("VACCINATIONS", s, theme_colors=theme_colors), sp(0.14)]
            story.append(para_row(
                "Proof of current vaccinations may be required. Please attach vet records if available.",
                s["note"]
            ))

            vax_col_widths = [VAX_COLUMNS["name"], VAX_COLUMNS["status"], VAX_COLUMNS["date"]]
            vax_data = [[
                Paragraph("Vaccine", s["th"]),
                Paragraph("Up to Date?", s["th"]),
                Paragraph("Expiration Date", s["th"]),
            ]]
            
            vaccines = [
                ("Rabies", "rabies", ["Yes", "No", "Exempt"]),
                ("DHPP / DA2PP", "dhpp", ["Yes", "No", "N/A"]),
                ("Bordetella (Kennel Cough)", "bordetella", ["Yes", "No", "N/A"]),
                ("Feline FVRCP", "fvrcp", ["Yes", "No", "N/A"]),
                ("Feline Leukemia", "felv", ["Yes", "No", "N/A"]),
                ("Canine Influenza", "canine_flu", ["Yes", "No", "N/A"]),
                ("Other", "other_vax", ["Yes", "No"]),
            ]
            
            if fillable:
                for vax_name, vax_key, options in vaccines:
                    field_base = f"{prefix}vax_{vax_key}"
                    checkbox_row = VaxCheckboxRow(field_base, options, theme_colors=theme_colors)
                    exp_field = FillableTextField(f"{field_base}_exp", vax_col_widths[2] - 16, height=18, theme_colors=theme_colors)
                    
                    if vax_key == "other_vax":
                        name_cell = [
                            Paragraph("Other: ", s["td"]),
                            FillableTextField(f"{prefix}vax_other_name", vax_col_widths[0] - 50, height=16, theme_colors=theme_colors),
                        ]
                        name_table = Table([name_cell], colWidths=[0.5*inch, vax_col_widths[0] - 50])
                        name_table.setStyle(TableStyle([
                            ("LEFTPADDING", (0,0), (-1,-1), 0),
                            ("RIGHTPADDING", (0,0), (-1,-1), 0),
                            ("TOPPADDING", (0,0), (-1,-1), 0),
                            ("BOTTOMPADDING", (0,0), (-1,-1), 0),
                            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                        ]))
                        vax_data.append([name_table, checkbox_row, exp_field])
                    else:
                        vax_data.append([Paragraph(vax_name, s["td"]), checkbox_row, exp_field])
            else:
                for vax_name, vax_key, options in vaccines:
                    opts_str = "   /   ".join(options)
                    display_name = vax_name if vax_key != "other_vax" else "Other: _______________"
                    vax_data.append([
                        Paragraph(display_name, s["td"]), 
                        Paragraph(opts_str, s["td"]), 
                        Paragraph("", s["td"])
                    ])

            vt = Table(vax_data, colWidths=vax_col_widths)
            vt.setStyle(TableStyle([
                ("BACKGROUND",    (0,0), (-1,0),  get_color(theme_colors, "primary")),
                ("GRID",          (0,0), (-1,-1), 0.4, get_color(theme_colors, "primary_mid")),
                ("ROWBACKGROUNDS",(0,1), (-1,-1), [get_color(theme_colors, "accent_light"), WHITE]),
                ("LEFTPADDING",   (0,0), (-1,-1), 8),
                ("TOPPADDING",    (0,0), (-1,-1), 8),
                ("BOTTOMPADDING", (0,0), (-1,-1), 8),
                ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
            ]))
            story.append(vt)
            if not fillable:
                story.append(para_row("Circle the appropriate response in each row.", s["note"]))

        has_page2_content = (sections["health_medications"] or 
                             sections["behavior_temperament"] or 
                             sections["feeding_daily_care"])
        
        if has_page2_content:
            story.append(PageBreak())
            current_page += 1
            story += pg_hdr(business_name, f"Page {current_page} of {total_pages}", s, theme_colors=theme_colors)
        
        if sections["health_medications"]:
            story += [sec_hdr(f"HEALTH & MEDICATIONS{pet_label}", s, theme_colors=theme_colors), sp(0.2)]

            story += field("Known Allergies or Sensitivities", s, extra_space=26, fillable=fillable,
                           field_name=f"{prefix}allergies", multiline=True, theme_colors=theme_colors)
            story += field("Medical Conditions / Diagnoses", s, extra_space=26, fillable=fillable,
                           field_name=f"{prefix}conditions", multiline=True, theme_colors=theme_colors)
            story.append(sp(0.1))
            story.append(para_row("Current Medications  <i>(name, dose, frequency, food instructions)</i>", s["lbl"]))
            story.append(sp(0.1))

            med_col_widths = [MED_COLUMNS["name"], MED_COLUMNS["dosage"], MED_COLUMNS["frequency"], MED_COLUMNS["instructions"]]
            med_data = [[
                Paragraph("Medication Name", s["th"]),
                Paragraph("Dosage", s["th"]),
                Paragraph("Frequency", s["th"]),
                Paragraph("Special Instructions", s["th"]),
            ]]
            
            if fillable:
                med_fields = ["med_name", "med_dosage", "med_frequency", "med_instructions"]
                for row_idx in range(3):
                    row = []
                    for col_idx, (fname, width) in enumerate(zip(med_fields, med_col_widths)):
                        field_name = f"{prefix}{fname}_{row_idx+1}"
                        row.append(FillableTextField(field_name, width - 16, height=20, theme_colors=theme_colors))
                    med_data.append(row)
            else:
                for _ in range(3):
                    med_data.append([Paragraph("", s["td"])] * 4)
            
            mt = Table(med_data, colWidths=med_col_widths)
            mt.setStyle(TableStyle([
                ("BACKGROUND",    (0,0), (-1,0),  get_color(theme_colors, "primary")),
                ("GRID",          (0,0), (-1,-1), 0.4, get_color(theme_colors, "primary_mid")),
                ("ROWBACKGROUNDS",(0,1), (-1,-1), [get_color(theme_colors, "accent_light"), WHITE, get_color(theme_colors, "accent_light")]),
                ("LEFTPADDING",   (0,0), (-1,-1), 8),
                ("TOPPADDING",    (0,0), (-1,-1), 14),
                ("BOTTOMPADDING", (0,0), (-1,-1), 14),
                ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
            ]))
            story.append(mt)
            story.append(sp(0.2))

        if sections["behavior_temperament"]:
            story += build_pet_behavior_section(s, pet_num, fillable=fillable, theme_colors=theme_colors)
            story.append(sp(0.15))
            story += build_potty_section(s, pet_num, fillable=fillable, theme_colors=theme_colors)
            story.append(sp(0.15))
            story += build_sleep_crate_section(s, pet_num, fillable=fillable, theme_colors=theme_colors)
            story.append(sp(0.2))

        if sections["feeding_daily_care"]:
            story += [sec_hdr(f"FEEDING & DAILY CARE{pet_label}", s, theme_colors=theme_colors), sp(0.2)]
            story.append(two_col("Food Brand / Type", "Amount per Meal", s, fillable=fillable,
                                 field_names=[f"{prefix}food_brand", f"{prefix}food_amount"], theme_colors=theme_colors))
            story += field("Where is food stored?", s, extra_space=22, fillable=fillable,
                           field_name=f"{prefix}food_location", theme_colors=theme_colors)

            story.append(para_row("Feeding Schedule:", s["lbl"]))
            if fillable:
                story.append(FillableCheckboxRow(f"{prefix}feeding_schedule",
                    ["Once daily", "Twice daily", "Three times daily", "Free-fed"], per_row=4, theme_colors=theme_colors))
            else:
                story.append(CheckboxRow(["Once daily", "Twice daily", "Three times daily", "Free-fed"], per_row=4, theme_colors=theme_colors))
            story.append(sp(0.16))

            story.append(para_row("Treats:", s["lbl"]))
            if fillable:
                story.append(FillableCheckboxRow(f"{prefix}treats",
                    ["Yes — allowed", "No — not allowed"], per_row=2, theme_colors=theme_colors))
            else:
                story.append(CheckboxRow(["Yes — allowed", "No — not allowed"], per_row=2, theme_colors=theme_colors))
            story.append(sp(0.1))

            story += field("If yes, treat brand / type & where stored:", s, extra_space=22, fillable=fillable,
                           field_name=f"{prefix}treat_info", theme_colors=theme_colors)
            story += field("Exercise needs (walk duration, activity level)", s, extra_space=22, fillable=fillable,
                           field_name=f"{prefix}exercise", multiline=True, theme_colors=theme_colors)
            story += field("Any other special care instructions", s, extra_lines=2, fillable=fillable,
                           field_name=f"{prefix}special_instructions", theme_colors=theme_colors)

    # ══════════════════════════════════════════════════════════════════════
    # SERVICE-SPECIFIC SECTION (if enabled and not general)
    # ══════════════════════════════════════════════════════════════════════
    if sections["service_specific"] and service_type != "general":
        story.append(PageBreak())
        current_page += 1
        story += pg_hdr(business_name, f"Page {current_page} of {total_pages}", s, theme_colors=theme_colors)
        story += build_service_specific_section(s, service_type, fillable=fillable, theme_colors=theme_colors)

    # ══════════════════════════════════════════════════════════════════════
    # AUTHORIZATION & SIGNATURE PAGE
    # ══════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    current_page += 1
    story += pg_hdr(business_name, f"Page {current_page} of {total_pages}", s, theme_colors=theme_colors)
    story += [sec_hdr("AUTHORIZATION & AGREEMENT", s, theme_colors=theme_colors), sp(0.18)]

    sitter = sitter_name if sitter_name else business_name
    for title, body in [
        ("Emergency Veterinary Care",
         f"I authorize <b>{sitter}</b> to seek emergency veterinary care for my pet(s) if I cannot "
         f"be reached and the situation requires immediate attention. I understand I am responsible "
         f"for all veterinary fees incurred."),
        ("Transport Authorization",
         f"I authorize <b>{sitter}</b> to transport my pet(s) in their vehicle if necessary for "
         f"veterinary care or other emergency situations."),
        ("Photo &amp; Social Media Release",
         f"I give permission for photos and videos of my pet(s) to be shared on social media or "
         f"used for marketing by <b>{sitter}</b>."),
        ("Cancellation Policy",
         "Please refer to our separate service agreement for cancellation and refund terms. By "
         "signing below, I acknowledge I have read and agree to all stated terms."),
        ("Liability",
         "I confirm my pet(s) is/are current on required vaccinations, has/have not shown "
         "aggression toward people or other animals without prior written disclosure, and I accept "
         "full liability for any damage or injury caused by my pet(s)."),
    ]:
        story.append(auth_block(title, body, s, theme_colors=theme_colors))
        story.append(sp(0.08))

    story.append(sp(0.06))
    story.append(para_row("Photo / video permission:", s["lbl"]))
    if fillable:
        story.append(FillableCheckboxRow("photo_permission",
            ["Yes, I give permission", "No, please do not share"], per_row=2, theme_colors=theme_colors))
    else:
        story.append(CheckboxRow(["Yes, I give permission", "No, please do not share"], per_row=2, theme_colors=theme_colors))
    story.append(sp(0.06))
    
    story.append(para_row("Transport authorization:", s["lbl"]))
    if fillable:
        story.append(FillableCheckboxRow("transport_permission",
            ["Yes, I authorize transport", "No, do not transport"], per_row=2, theme_colors=theme_colors))
    else:
        story.append(CheckboxRow(["Yes, I authorize transport", "No, do not transport"], per_row=2, theme_colors=theme_colors))
    story.append(sp(0.2))

    story.append(two_col("Client Signature", "Date", s, fillable=fillable,
                         field_names=["signature", "signature_date"], theme_colors=theme_colors))
    story.append(sp(0.1))
    story += field("Printed Name", s, fillable=fillable, field_name="printed_name", theme_colors=theme_colors)
    story.append(sp(0.2))

    ot = Table([[Paragraph(
        "For office use only  \u00b7  Client ID: _________________   Date on file: _________________   "
        "Last updated: _________________",
        s["office"]
    )]], colWidths=[PAGE_W])
    ot.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), get_color(theme_colors, "primary")),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
    ]))
    story.append(ot)
    story.append(sp(0.15))
    story.append(hr(theme_colors, 0.8, 6))
    story.append(Paragraph(f"{business_name}  \u00b7  {location}  \u00b7  {contact}", s["foot"]))
    story.append(Paragraph("Thank you for trusting us with your furry family member!", s["foot"]))

    doc.build(story)
    theme_name = config.get("theme", "lavender")
    print(f"✅  Form saved to: {output_path}")
    print(f"   Pages: {total_pages}, Pets: {num_pets}, Service type: {service_type}, Theme: {theme_name}")
    if fillable:
        print("   📝 Fillable PDF fields enabled")
    
    enabled = [sec for sec, v in sections.items() if v]
    disabled = [sec for sec, v in sections.items() if not v]
    if disabled:
        print(f"   Sections: {', '.join(enabled)}")
        print(f"   Excluded: {', '.join(disabled)}")
