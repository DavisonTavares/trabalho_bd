from django import template

register = template.Library()

@register.filter(name='format_volume')
def format_volume(value):
    try:
        value = float(value)
    except (ValueError, TypeError):
        return value  # Retorna o valor original se não puder ser convertido
    
    if value < 1:
        return f"{(value * 1000):.0f} ml"
    else:
        # Verifica se o valor é inteiro
        if value.is_integer():
            return f"{int(value)} L"
        else:
            return f"{value:.2f} L"

@register.filter(name='format_number_input')
def format_number_input(value):
    try:
        # transforma o valor float em string
        value = str(value)
        value = value.replace('.', ',')
        value = float(value)
    except (ValueError, TypeError):
        return value
    