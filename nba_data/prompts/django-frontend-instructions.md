# Django Frontend Instructions

Follow these instructions to create new frontend components using the HTMX + Alpine.js + Tailwind CSS stack.

## Guidelines

### Project Structure
- Django templates are stored in `templates/` directory of each app or in a project-level `templates/` directory
- Place reusable template components in `templates/components/` directory
- Store static assets (CSS, JS) in the `static/` directory
- Use Django's template inheritance system with a base layout (`base.html`)

### Template Components
- Create partial templates for reusable UI components
- Name partial templates with a leading underscore (e.g., `_navbar.html`, `_sidebar.html`)
- Include components using Django's include tag: `{% include "components/_button.html" with label="Submit" %}`

### HTMX Integration
- Add HTMX via CDN or in your static files
- Create Django views that return partial HTML for HTMX requests
- Use the `hx-` attributes in templates to enable HTMX functionality:
  - `hx-get`, `hx-post`, `hx-put`, `hx-delete` for AJAX requests
  - `hx-target` to specify where to swap content
  - `hx-swap` to determine how content is swapped
  - `hx-trigger` to specify the triggering event

### Alpine.js Components
- Add Alpine.js via CDN or in your static files
- Use `x-data` to define component state
- Use Alpine directives for interactivity:
  - `x-show`, `x-if`, `x-for` for conditional rendering
  - `@click`, `@input` for event handling
  - `x-bind` or `:` for attribute binding
  - `x-model` for two-way binding

### Tailwind CSS Usage
- Use Django-Tailwind for Tailwind CSS integration
- Apply utility classes directly in HTML templates
- Create custom components by combining Tailwind utility classes
- Extract common patterns into Django template includes or template tags

### View Structure
- Standard views return full HTML pages
- HTMX views return partial HTML fragments
- For HTMX requests, check for the `HX-Request` header:
  ```python
  if request.headers.get('HX-Request'):
      # Return partial template for HTMX request
      return render(request, 'partials/_item_list.html', context)
  else:
      # Return full page for normal request
      return render(request, 'full_page.html', context)
  ```

### Response Headers
- Use Django's `HttpResponse` headers for HTMX-specific behaviors:
  ```python
  response = render(request, 'partials/_form.html', context)
  response['HX-Trigger'] = '{"showMessage": "Item created successfully"}'
  return response
  ```

### Forms
- Use Django forms with HTMX for dynamic form submission
- Add `hx-post` to form tags for AJAX form submission
- Return validation errors in partial templates

### Common Patterns
- Lazy loading: Use `hx-get` with `load` trigger
- Infinite scroll: Use `hx-get` with `intersect` trigger
- Form validation: Use `hx-post` with validation feedback
- Search-as-you-type: Use `hx-get` with `input` trigger and debounce
- Modals/dialogs: Use Alpine.js for state management and HTMX for content loading
