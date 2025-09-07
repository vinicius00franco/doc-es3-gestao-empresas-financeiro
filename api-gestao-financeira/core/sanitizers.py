import html
import re
from django.utils.html import strip_tags


def sanitize_text_input(text):
    """
    Sanitiza entrada de texto para prevenir XSS
    """
    if not text:
        return text
    
    # Remove tags HTML
    text = strip_tags(text)
    
    # Escapa caracteres HTML
    text = html.escape(text)
    
    # Remove caracteres de controle
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    return text.strip()


def sanitize_filename(filename):
    """
    Sanitiza nome de arquivo
    """
    if not filename:
        return filename
    
    # Remove caracteres perigosos
    filename = re.sub(r'[^\w\s.-]', '', filename)
    
    # Remove múltiplos pontos consecutivos
    filename = re.sub(r'\.{2,}', '.', filename)
    
    return filename.strip()


def validate_cnpj_format(cnpj):
    """
    Valida formato de CNPJ
    """
    if not cnpj:
        return False
    
    # Remove tudo que não é dígito
    digits_only = re.sub(r'\D', '', cnpj)
    
    # Verifica se tem 14 dígitos
    return len(digits_only) == 14