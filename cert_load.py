
import os
import requests
import logging
from OpenSSL import crypto

logger = logging.getLogger(__name__)

def ensure_ca_certificate() -> str:
    cert_url = "http://secure.globalsign.com/cacert/gsgccr3dvtlsca2020.crt"
    cert_path = "gsgccr3dvtlsca2020.pem"
    
    if os.path.exists(cert_path):
        logger.info(f"Сертификат уже существует: {cert_path}")
        return cert_path
    
    try:
        logger.info(f"Загрузка сертификата с {cert_url}")
        response = requests.get(cert_url, timeout=5)
        response.raise_for_status()
        
        cert_der = response.content
        cert = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_der)
        cert_pem = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
        
        with open(cert_path, "wb") as f:
            f.write(cert_pem)
        logger.info(f"Сертификат сохранен: {cert_path}")
        return cert_path
    except Exception as e:
        logger.error(f"Ошибка загрузки сертификата: {e}")
        raise