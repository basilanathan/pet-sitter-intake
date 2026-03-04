# Screenshots for ClawHub

Generate these screenshots before submitting to ClawHub. Requirements:
- Resolution: 1920x1080 or 1280x720
- Format: PNG
- Use real data, not placeholder text

## Required Screenshots

### 1. `01-generated-form.png` (Hero Shot)
Full page view of a generated PDF showing the pet owner information section.

```bash
python scripts/generate_form.py \
  --business-name "Happy Paws Pet Sitting" \
  --sitter-name "Jane Smith" \
  --services "Dog Walking, Boarding, Drop-in Visits" \
  --location "Austin, TX" \
  --contact "jane@happypaws.com | (512) 555-1234" \
  --theme ocean \
  --output screenshots/demo-ocean.pdf
```

Open the PDF and screenshot the first page.

### 2. `02-themes-comparison.png`
Side-by-side comparison of 3-4 themes (lavender, ocean, forest, sunset).

Generate multiple PDFs with different themes, then create a composite image.

```bash
for theme in lavender ocean forest sunset; do
  python scripts/generate_form.py \
    --business-name "Demo Business" \
    --theme $theme \
    --output screenshots/demo-$theme.pdf
done
```

### 3. `03-fillable-fields.png`
Show the PDF open in a viewer with cursor in a fillable text field, demonstrating interactivity.

### 4. `04-multi-pet.png` (Optional)
Show a form generated with `--pets 3` displaying multiple pet profile sections.

### 5. `05-vaccination-checkboxes.png` (Optional)
Close-up of the vaccination section showing interactive checkboxes.

## Tips

- Use a clean PDF viewer (Preview on macOS, Adobe Reader)
- Zoom to ~100% for crisp text
- Crop to focus on relevant content
- For comparison shots, use a tool like Figma or Photoshop to arrange side-by-side
