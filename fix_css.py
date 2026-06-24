import re

with open('app/static/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove all backticks 
cleaned = re.sub(r'```', '', content)
# Clean up multiple blank lines
cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)

with open('app/static/style.css', 'w', encoding='utf-8') as f:
    f.write(cleaned)

# Verify
with open('app/static/style.css', 'r') as f:
    result = f.read()
    backtick_count = result.count('`')
    print(f"CSS file cleaned. Backticks remaining: {backtick_count}")
