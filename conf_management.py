import config as cfg


def get_pass(prod_env) -> str:
    if prod_env:
        return cfg.PRO_PASS
    else:
        return cfg.SANDBOX_PASS

def get_user(prod_env) -> str:
    if prod_env:
        return cfg.PRO_USER
    else:
        return cfg.SANDBOX_USER

def get_endpoint_consulta_colas(prod_env) -> str:
    if prod_env:
        return cfg.PRO_ENDPOINT_COLAS
    else:
        return cfg.SANDBOX_ENDPOINT_COLAS

def get_endpoint_activar_colas(prod_env) -> str:
    if prod_env:
        return cfg.PRO_ENDPOINT_ACTIVAR
    else:
        return cfg.SANDBOX_ENDPOINT_ACTIVAR

