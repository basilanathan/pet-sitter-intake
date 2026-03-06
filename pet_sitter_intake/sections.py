"""Section builders for intake form pages."""

from .flowables import CheckboxRow, FillableCheckboxRow
from .layout import sec_hdr, sp, para_row, field


def build_home_access_section(s, fillable=False):
    """Home access section for in-home pet sitting.
    
    Args:
        s: Styles dict from sty()
        fillable: Whether to generate interactive form fields
    """
    elements = []
    elements += [sec_hdr("HOME ACCESS & PROPERTY INFORMATION", s), sp(0.2)]
    
    elements.append(para_row("Key / Entry Information", s["sublbl"]))
    elements.append(sp(0.1))
    
    elements.append(para_row("Entry method:", s["lbl"]))
    if fillable:
        elements.append(FillableCheckboxRow("entry_method", 
            ["Key provided", "Lockbox", "Garage code", "Door code", "Hidden key", "Other"],
            per_row=3
        ))
    else:
        elements.append(CheckboxRow(
            ["Key provided", "Lockbox", "Garage code", "Door code", "Hidden key", "Other"],
            per_row=3
        ))
    elements.append(sp(0.1))
    
    elements += field("Lockbox / key location", s, fillable=fillable, field_name="key_location")
    elements += field("Entry code(s)", s, fillable=fillable, field_name="entry_codes")
    elements += field("Alarm code & disarm instructions", s, fillable=fillable, field_name="alarm_code", multiline=True)
    elements.append(sp(0.12))
    
    elements.append(para_row("Property Details", s["sublbl"]))
    elements.append(sp(0.1))
    elements += field("WiFi network & password", s, fillable=fillable, field_name="wifi_info")
    elements += field("Parking instructions", s, fillable=fillable, field_name="parking", multiline=True)
    elements += field("Thermostat / HVAC notes", s, fillable=fillable, field_name="thermostat", multiline=True)
    elements += field("Off-limits rooms or areas", s, fillable=fillable, field_name="off_limits")
    elements += field("Other house rules (TV on for pet, mail, plants, etc.)", s, extra_lines=2, 
                      fillable=fillable, field_name="house_rules")
    
    return elements


def build_pet_behavior_section(s, pet_num=1, fillable=False):
    """Enhanced pet behavior and temperament section.
    
    Args:
        s: Styles dict from sty()
        pet_num: Pet number for multi-pet forms (used for field name prefixes)
        fillable: Whether to generate interactive form fields
    """
    prefix = f"pet{pet_num}_" if pet_num > 1 else ""
    elements = []
    
    elements += [sec_hdr("BEHAVIOR & TEMPERAMENT", s), sp(0.2)]
    
    elements.append(para_row("Good with:", s["lbl"]))
    if fillable:
        elements.append(FillableCheckboxRow(f"{prefix}good_with",
            ["Strangers", "Children", "Other dogs", "Cats", "Small animals"],
            per_row=5
        ))
    else:
        elements.append(CheckboxRow(
            ["Strangers", "Children", "Other dogs", "Cats", "Small animals"],
            per_row=5
        ))
    elements.append(sp(0.1))
    
    elements.append(para_row("Known fears / triggers:", s["lbl"]))
    if fillable:
        elements.append(FillableCheckboxRow(f"{prefix}fears",
            ["Thunderstorms", "Fireworks", "Vacuum", "Doorbell", "Men", "Hats/uniforms", "None known"],
            per_row=4
        ))
    else:
        elements.append(CheckboxRow(
            ["Thunderstorms", "Fireworks", "Vacuum", "Doorbell", "Men", "Hats/uniforms", "None known"],
            per_row=4
        ))
    elements.append(sp(0.1))
    
    elements += field("Other triggers or sensitivities", s, fillable=fillable, 
                      field_name=f"{prefix}other_triggers", multiline=True)
    
    elements.append(para_row("Separation anxiety:", s["lbl"]))
    if fillable:
        elements.append(FillableCheckboxRow(f"{prefix}separation",
            ["None", "Mild (whines)", "Moderate (barks/paces)", "Severe (destructive)"],
            per_row=4
        ))
    else:
        elements.append(CheckboxRow(
            ["None", "Mild (whines)", "Moderate (barks/paces)", "Severe (destructive)"],
            per_row=4
        ))
    elements.append(sp(0.1))
    
    elements.append(para_row("Escape artist?", s["lbl"]))
    if fillable:
        elements.append(FillableCheckboxRow(f"{prefix}escape",
            ["No", "Yes — door dasher", "Yes — fence jumper/digger", "Yes — gate opener"],
            per_row=4
        ))
    else:
        elements.append(CheckboxRow(
            ["No", "Yes — door dasher", "Yes — fence jumper/digger", "Yes — gate opener"],
            per_row=4
        ))
    elements.append(sp(0.1))
    
    elements += field("Commands pet knows (sit, stay, come, etc.)", s, fillable=fillable,
                      field_name=f"{prefix}commands")
    elements += field("Recall reliability off-leash (1-10, or N/A)", s, fillable=fillable,
                      field_name=f"{prefix}recall")
    
    return elements


def build_potty_section(s, pet_num=1, fillable=False):
    """Potty and house-training section.
    
    Args:
        s: Styles dict from sty()
        pet_num: Pet number for multi-pet forms
        fillable: Whether to generate interactive form fields
    """
    prefix = f"pet{pet_num}_" if pet_num > 1 else ""
    elements = []
    
    elements.append(para_row("Potty / House Training", s["sublbl"]))
    elements.append(sp(0.1))
    
    elements.append(para_row("Potty trained?", s["lbl"]))
    if fillable:
        elements.append(FillableCheckboxRow(f"{prefix}potty_trained",
            ["Fully trained", "Mostly (occasional accidents)", "In progress", "Uses pads/litter"],
            per_row=4
        ))
    else:
        elements.append(CheckboxRow(
            ["Fully trained", "Mostly (occasional accidents)", "In progress", "Uses pads/litter"],
            per_row=4
        ))
    elements.append(sp(0.1))
    
    elements += field("Potty schedule / signals they give when needing to go", s, fillable=fillable,
                      field_name=f"{prefix}potty_schedule", multiline=True)
    elements += field("Preferred potty area (backyard spot, specific walk route, etc.)", s, 
                      fillable=fillable, field_name=f"{prefix}potty_area", multiline=True)
    
    return elements


def build_sleep_crate_section(s, pet_num=1, fillable=False):
    """Sleep and crate training section.
    
    Args:
        s: Styles dict from sty()
        pet_num: Pet number for multi-pet forms
        fillable: Whether to generate interactive form fields
    """
    prefix = f"pet{pet_num}_" if pet_num > 1 else ""
    elements = []
    
    elements.append(para_row("Sleep & Crate", s["sublbl"]))
    elements.append(sp(0.1))
    
    elements.append(para_row("Where does pet sleep?", s["lbl"]))
    if fillable:
        elements.append(FillableCheckboxRow(f"{prefix}sleep_location",
            ["Own bed", "Crate", "Owner's bed", "Couch", "Anywhere"],
            per_row=5
        ))
    else:
        elements.append(CheckboxRow(
            ["Own bed", "Crate", "Owner's bed", "Couch", "Anywhere"],
            per_row=5
        ))
    elements.append(sp(0.1))
    
    elements.append(para_row("Crate trained?", s["lbl"]))
    if fillable:
        elements.append(FillableCheckboxRow(f"{prefix}crate_trained",
            ["Yes — loves it", "Yes — tolerates it", "No — do not crate", "N/A"],
            per_row=4
        ))
    else:
        elements.append(CheckboxRow(
            ["Yes — loves it", "Yes — tolerates it", "No — do not crate", "N/A"],
            per_row=4
        ))
    elements.append(sp(0.1))
    
    elements += field("Crate location / bedtime routine", s, fillable=fillable,
                      field_name=f"{prefix}bedtime_routine", multiline=True)
    
    return elements


def build_service_specific_section(s, service_type, fillable=False):
    """Service-specific fields based on service type.
    
    Args:
        s: Styles dict from sty()
        service_type: One of 'walking', 'boarding', 'drop_in'
        fillable: Whether to generate interactive form fields
    """
    elements = []
    
    if service_type == "walking":
        elements += [sec_hdr("DOG WALKING DETAILS", s), sp(0.2)]
        elements += field("Leash & harness location", s, fillable=fillable, field_name="leash_location")
        elements += field("Poop bag location", s, fillable=fillable, field_name="poop_bags")
        
        elements.append(para_row("Leash behavior:", s["lbl"]))
        if fillable:
            elements.append(FillableCheckboxRow("leash_behavior",
                ["Loose leash", "Pulls — needs management", "Reactive on leash", "Heel trained"],
                per_row=4
            ))
        else:
            elements.append(CheckboxRow(
                ["Loose leash", "Pulls — needs management", "Reactive on leash", "Heel trained"],
                per_row=4
            ))
        elements.append(sp(0.1))
        
        elements += field("Preferred walking route / areas to avoid", s, fillable=fillable,
                          field_name="walk_route", multiline=True)
        elements += field("Walk duration preference", s, fillable=fillable, field_name="walk_duration")
        
    elif service_type == "boarding":
        elements += [sec_hdr("BOARDING DETAILS", s), sp(0.2)]
        
        elements.append(para_row("Items to bring:", s["lbl"]))
        if fillable:
            elements.append(FillableCheckboxRow("boarding_items",
                ["Food", "Bed/blanket", "Favorite toys", "Medications", "Crate", "Treats"],
                per_row=3
            ))
        else:
            elements.append(CheckboxRow(
                ["Food", "Bed/blanket", "Favorite toys", "Medications", "Crate", "Treats"],
                per_row=3
            ))
        elements.append(sp(0.1))
        
        elements += field("Drop-off date & time", s, fillable=fillable, field_name="dropoff_datetime")
        elements += field("Pick-up date & time", s, fillable=fillable, field_name="pickup_datetime")
        elements += field("Special items or comfort objects", s, fillable=fillable, 
                          field_name="comfort_items")
        
    elif service_type == "drop_in":
        elements += [sec_hdr("DROP-IN VISIT DETAILS", s), sp(0.2)]
        
        elements.append(para_row("Tasks per visit (check all that apply):", s["lbl"]))
        if fillable:
            elements.append(FillableCheckboxRow("dropin_tasks",
                ["Feed", "Fresh water", "Potty break/walk", "Playtime", "Medication", 
                 "Scoop litter", "Bring in mail", "Water plants", "Rotate lights"],
                per_row=3
            ))
        else:
            elements.append(CheckboxRow(
                ["Feed", "Fresh water", "Potty break/walk", "Playtime", "Medication", 
                 "Scoop litter", "Bring in mail", "Water plants", "Rotate lights"],
                per_row=3
            ))
        elements.append(sp(0.1))
        
        elements += field("Visit time preference", s, fillable=fillable, field_name="visit_time")
        elements += field("Visit duration needed", s, fillable=fillable, field_name="visit_duration")
    
    return elements
