"""Pet profile pages: profile, vaccinations, health, behavior, feeding."""

from reportlab.platypus import Table, TableStyle, Paragraph, PageBreak

from ..constants import (
    PAGE_W, WHITE, VAX_COLUMNS, MED_COLUMNS, PET_PROFILE_COLUMNS,
)
from ..flowables import (
    FillableTextField, VaxCheckboxRow, get_color,
)
from ..layout import sec_hdr, sp, para_row, field, two_col, three_col, pg_hdr

from .context import FormContext


def build_pet_basic_info(ctx: FormContext, pet_num: int) -> list:
    """Build basic pet info: name, breed, age, sex, microchip.
    
    Args:
        ctx: Form context
        pet_num: Pet number (1-indexed)
        
    Returns:
        List of flowables
    """
    s = ctx.styles
    tc = ctx.theme_colors
    fillable = ctx.fillable
    prefix = ctx.pet_field_name("", pet_num).rstrip("_")  # "pet2" or ""
    prefix = f"{prefix}_" if prefix else ""
    elements = []
    
    elements.append(two_col("Pet Name", "Species  (Dog / Cat / Other)", s, fillable=fillable,
                            field_names=[f"{prefix}name", f"{prefix}species"], theme_colors=tc))
    elements.append(two_col("Breed", "Mix?   Yes  /  No", s, fillable=fillable,
                            field_names=[f"{prefix}breed", f"{prefix}mix"], theme_colors=tc))
    elements.append(three_col(
        ["Age", "Weight (lbs)", "Color / Markings"], s,
        widths=[PET_PROFILE_COLUMNS["age"], PET_PROFILE_COLUMNS["weight"], PET_PROFILE_COLUMNS["color"]],
        fillable=fillable,
        field_names=[f"{prefix}age", f"{prefix}weight", f"{prefix}color_markings"],
        theme_colors=tc
    ))
    
    elements.append(para_row("Sex:", s["lbl"]))
    elements.append(ctx.checkbox_row(
        ["Male (intact)", "Male (neutered)", "Female (intact)", "Female (spayed)"],
        field_prefix=f"{prefix}sex",
        per_row=4
    ))
    elements.append(sp(0.12))
    
    elements.append(two_col("Microchip #", "License / Tag #", s, fillable=fillable,
                            field_names=[f"{prefix}microchip", f"{prefix}license"], theme_colors=tc))
    elements.append(sp(0.15))
    
    # Flea/tick prevention
    elements.append(para_row("Flea/Tick Prevention", s["sublbl"]))
    elements.append(sp(0.1))
    elements.append(two_col("Prevention product used", "Last applied date", s, fillable=fillable,
                            field_names=[f"{prefix}flea_product", f"{prefix}flea_date"], theme_colors=tc))
    elements.append(sp(0.15))
    
    return elements


def build_vaccinations_section(ctx: FormContext, pet_num: int) -> list:
    """Build vaccination records table.
    
    Args:
        ctx: Form context
        pet_num: Pet number (1-indexed)
        
    Returns:
        List of flowables
    """
    if not ctx.section_enabled("vaccinations"):
        return []
    
    s = ctx.styles
    tc = ctx.theme_colors
    fillable = ctx.fillable
    prefix = ctx.pet_field_name("", pet_num).rstrip("_")
    prefix = f"{prefix}_" if prefix else ""
    elements = []
    
    elements += [sec_hdr("VACCINATIONS", s, theme_colors=tc), sp(0.14)]
    elements.append(para_row(
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
            checkbox_row = VaxCheckboxRow(field_base, options, theme_colors=tc)
            exp_field = FillableTextField(f"{field_base}_exp", vax_col_widths[2] - 16, 
                                          height=18, theme_colors=tc)
            
            if vax_key == "other_vax":
                from reportlab.lib.units import inch
                name_cell = [
                    Paragraph("Other: ", s["td"]),
                    FillableTextField(f"{prefix}vax_other_name", vax_col_widths[0] - 50,
                                      height=16, theme_colors=tc),
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
        ("BACKGROUND",    (0,0), (-1,0),  get_color(tc, "primary")),
        ("GRID",          (0,0), (-1,-1), 0.4, get_color(tc, "primary_mid")),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [get_color(tc, "accent_light"), WHITE]),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    elements.append(vt)
    
    if not fillable:
        elements.append(para_row("Circle the appropriate response in each row.", s["note"]))
    
    return elements


def build_health_medications_section(ctx: FormContext, pet_num: int) -> list:
    """Build health and medications section with table.
    
    Args:
        ctx: Form context
        pet_num: Pet number (1-indexed)
        
    Returns:
        List of flowables
    """
    if not ctx.section_enabled("health_medications"):
        return []
    
    s = ctx.styles
    tc = ctx.theme_colors
    fillable = ctx.fillable
    prefix = ctx.pet_field_name("", pet_num).rstrip("_")
    prefix = f"{prefix}_" if prefix else ""
    pet_label = ctx.pet_label(pet_num)
    elements = []
    
    elements += [sec_hdr(f"HEALTH & MEDICATIONS{pet_label}", s, theme_colors=tc), sp(0.2)]
    
    elements += field("Known Allergies or Sensitivities", s, extra_space=26, fillable=fillable,
                      field_name=f"{prefix}allergies", multiline=True, theme_colors=tc)
    elements += field("Medical Conditions / Diagnoses", s, extra_space=26, fillable=fillable,
                      field_name=f"{prefix}conditions", multiline=True, theme_colors=tc)
    elements.append(sp(0.1))
    elements.append(para_row("Current Medications  <i>(name, dose, frequency, food instructions)</i>", s["lbl"]))
    elements.append(sp(0.1))
    
    med_col_widths = [MED_COLUMNS["name"], MED_COLUMNS["dosage"], 
                     MED_COLUMNS["frequency"], MED_COLUMNS["instructions"]]
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
                row.append(FillableTextField(field_name, width - 16, height=20, theme_colors=tc))
            med_data.append(row)
    else:
        for _ in range(3):
            med_data.append([Paragraph("", s["td"])] * 4)
    
    mt = Table(med_data, colWidths=med_col_widths)
    mt.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  get_color(tc, "primary")),
        ("GRID",          (0,0), (-1,-1), 0.4, get_color(tc, "primary_mid")),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [get_color(tc, "accent_light"), WHITE, get_color(tc, "accent_light")]),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("TOPPADDING",    (0,0), (-1,-1), 14),
        ("BOTTOMPADDING", (0,0), (-1,-1), 14),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    elements.append(mt)
    elements.append(sp(0.2))
    
    return elements


def build_feeding_section(ctx: FormContext, pet_num: int) -> list:
    """Build feeding and daily care section.
    
    Args:
        ctx: Form context
        pet_num: Pet number (1-indexed)
        
    Returns:
        List of flowables
    """
    if not ctx.section_enabled("feeding_daily_care"):
        return []
    
    s = ctx.styles
    tc = ctx.theme_colors
    fillable = ctx.fillable
    prefix = ctx.pet_field_name("", pet_num).rstrip("_")
    prefix = f"{prefix}_" if prefix else ""
    pet_label = ctx.pet_label(pet_num)
    elements = []
    
    elements += [sec_hdr(f"FEEDING & DAILY CARE{pet_label}", s, theme_colors=tc), sp(0.2)]
    
    elements.append(two_col("Food Brand / Type", "Amount per Meal", s, fillable=fillable,
                            field_names=[f"{prefix}food_brand", f"{prefix}food_amount"], theme_colors=tc))
    elements += field("Where is food stored?", s, extra_space=22, fillable=fillable,
                      field_name=f"{prefix}food_location", theme_colors=tc)
    
    elements.append(para_row("Feeding Schedule:", s["lbl"]))
    elements.append(ctx.checkbox_row(
        ["Once daily", "Twice daily", "Three times daily", "Free-fed"],
        field_prefix=f"{prefix}feeding_schedule",
        per_row=4
    ))
    elements.append(sp(0.16))
    
    elements.append(para_row("Treats:", s["lbl"]))
    elements.append(ctx.checkbox_row(
        ["Yes — allowed", "No — not allowed"],
        field_prefix=f"{prefix}treats",
        per_row=2
    ))
    elements.append(sp(0.1))
    
    elements += field("If yes, treat brand / type & where stored:", s, extra_space=22, fillable=fillable,
                      field_name=f"{prefix}treat_info", theme_colors=tc)
    elements += field("Exercise needs (walk duration, activity level)", s, extra_space=22, fillable=fillable,
                      field_name=f"{prefix}exercise", multiline=True, theme_colors=tc)
    elements += field("Any other special care instructions", s, extra_lines=2, fillable=fillable,
                      field_name=f"{prefix}special_instructions", theme_colors=tc)
    
    return elements


def build_pet_profile_page1(ctx: FormContext, pet_num: int) -> list:
    """Build first page of pet profile (basic info + vaccinations).
    
    Args:
        ctx: Form context
        pet_num: Pet number (1-indexed)
        
    Returns:
        List of flowables including PageBreak
    """
    s = ctx.styles
    tc = ctx.theme_colors
    pet_label = ctx.pet_label(pet_num)
    elements = []
    
    elements.append(PageBreak())
    ctx.next_page()
    elements += pg_hdr(ctx.business_name, ctx.page_label(), s, theme_colors=tc)
    elements += [sec_hdr(f"PET PROFILE{pet_label}", s, theme_colors=tc), sp(0.2)]
    
    if ctx.num_pets > 1:
        elements.append(para_row(f"<b>Pet {pet_num} of {ctx.num_pets}</b>", s["note"]))
    
    elements += build_pet_basic_info(ctx, pet_num)
    elements += build_vaccinations_section(ctx, pet_num)
    
    return elements


def build_pet_profile_page2(ctx: FormContext, pet_num: int) -> list:
    """Build second page of pet profile (health, behavior, feeding).
    
    Args:
        ctx: Form context
        pet_num: Pet number (1-indexed)
        
    Returns:
        List of flowables including PageBreak (if needed)
    """
    # Import behavior sections from sections module
    from ..sections import (
        build_pet_behavior_section, build_potty_section, build_sleep_crate_section
    )
    
    s = ctx.styles
    tc = ctx.theme_colors
    fillable = ctx.fillable
    elements = []
    
    has_content = (ctx.section_enabled("health_medications") or
                   ctx.section_enabled("behavior_temperament") or
                   ctx.section_enabled("feeding_daily_care"))
    
    if not has_content:
        return []
    
    elements.append(PageBreak())
    ctx.next_page()
    elements += pg_hdr(ctx.business_name, ctx.page_label(), s, theme_colors=tc)
    
    elements += build_health_medications_section(ctx, pet_num)
    
    if ctx.section_enabled("behavior_temperament"):
        elements += build_pet_behavior_section(s, pet_num, fillable=fillable, theme_colors=tc)
        elements.append(sp(0.15))
        elements += build_potty_section(s, pet_num, fillable=fillable, theme_colors=tc)
        elements.append(sp(0.15))
        elements += build_sleep_crate_section(s, pet_num, fillable=fillable, theme_colors=tc)
        elements.append(sp(0.2))
    
    elements += build_feeding_section(ctx, pet_num)
    
    return elements


def build_all_pet_profiles(ctx: FormContext) -> list:
    """Build all pet profile pages for all pets.
    
    Args:
        ctx: Form context
        
    Returns:
        List of flowables for all pet pages
    """
    elements = []
    for pet_num in range(1, ctx.num_pets + 1):
        elements += build_pet_profile_page1(ctx, pet_num)
        elements += build_pet_profile_page2(ctx, pet_num)
    return elements
