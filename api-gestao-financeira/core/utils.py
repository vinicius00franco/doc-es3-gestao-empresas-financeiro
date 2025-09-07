import os
from django.conf import settings
from django.utils._os import safe_join
from werkzeug.utils import secure_filename


def get_safe_file_path(filename, subfolder=''):
    """
    Retorna um caminho seguro para arquivo, prevenindo path traversal
    """
    # Sanitizar nome do arquivo
    safe_name = secure_filename(filename)
    if not safe_name:
        raise ValueError("Nome de arquivo inválido")
    
    # Construir caminho seguro
    if subfolder:
        base_path = safe_join(settings.MEDIA_ROOT, subfolder)
    else:
        base_path = settings.MEDIA_ROOT
    
    # Garantir que o diretório existe
    os.makedirs(base_path, exist_ok=True)
    
    # Retornar caminho seguro
    return safe_join(base_path, safe_name)


def validate_file_path(file_path):
    """
    Valida se o caminho do arquivo está dentro do diretório permitido
    """
    try:
        # Normalizar caminhos
        file_path = os.path.normpath(file_path)
        media_root = os.path.normpath(settings.MEDIA_ROOT)
        
        # Verificar se está dentro do MEDIA_ROOT
        return file_path.startswith(media_root)
    except (ValueError, TypeError):
        return False