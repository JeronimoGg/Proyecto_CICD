import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.getcwd())

# Importar y ejecutar pytest
import pytest

if __name__ == "__main__":
    pytest.main()
