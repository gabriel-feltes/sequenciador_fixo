import logging

# Configuração de logs
logging.basicConfig(filename="backend.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_event(message):
    """Registra eventos importantes no log."""
    logging.info(message)
    print(message)  # Também imprime no console para depuração