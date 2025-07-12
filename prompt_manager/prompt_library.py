# -*- coding: utf-8 -*-
SPECIALIZED_PROMPTS = {
    'python': {'name': 'Python', 'prompt': "\n### Python Expertise\n- **Style:** Write clean, PEP 8 compliant Pythonic code.\n- **Modern Features:** Use type hints, f-strings, and list comprehensions.\n"},
    'django': {'name': 'Django', 'prompt': "\n### Django Expertise\n- **Architecture:** Follow Django's design patterns (Fat Models, Thin Views).\n- **ORM:** Use `select_related` and `prefetch_related` to optimize queries.\n"},
    'odoo': {'name': 'Odoo', 'prompt': "\n### Odoo 18 Expertise\n- **Views:** Use `<list>` instead of `<tree>`.\n- **Images:** Use `product_template_image_ids` for image galleries.\n"},
    'wordpress': {'name': 'WordPress', 'prompt': "\n### WordPress Expertise\n- **Core:** Proficient with Hooks (actions/filters) and core APIs.\n- **Security:** Sanitize all inputs and escape all outputs. Use nonces.\n"},
    'php': {'name': 'PHP', 'prompt': "\n### PHP Expertise\n- **Modern PHP:** Write code for PHP 8+ using strict types.\n- **Standards:** Follow PSR coding standards.\n"},
    'javascript': {'name': 'JavaScript', 'prompt': "\n### JavaScript Expertise\n- **Modern JS:** Use ES6+ features like `async/await` and `const/let`.\n- **Best Practices:** Write modular and maintainable code.\n"},
    'ui_ux': {'name': 'UI/UX Design', 'prompt': "\n### UI/UX Design Expertise\n- **User-Centric:** Prioritize intuitive, efficient, and accessible user experiences.\n- **Principles:** Apply core design principles like hierarchy and contrast.\n"},
}
def generate_system_prompt(technologies_list, custom_text=""):
    if not isinstance(technologies_list, list):
        technologies_list = [tech.strip() for tech in technologies_list.split(',') if tech.strip()]
    
    selected_tech_names = [SPECIALIZED_PROMPTS[tech]['name'] for tech in technologies_list if tech in SPECIALIZED_PROMPTS]
    intro = f"You are a senior developer, an expert in: {', '.join(selected_tech_names)}." if selected_tech_names else "You are a helpful assistant."
    
    prompt_parts = [intro]
    for tech in technologies_list:
        if tech in SPECIALIZED_PROMPTS:
            prompt_parts.append(SPECIALIZED_PROMPTS[tech]['prompt'])
    if custom_text:
        prompt_parts.append("\n### Project-Specific Instructions\n" + custom_text)
    return "\n".join(prompt_parts)
