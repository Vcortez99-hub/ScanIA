import requests
import ssl
import socket
from urllib.parse import urlparse
from typing import Dict, Any, List

class SecurityHeadersScanner:
    """Scanner para análise de cabeçalhos de segurança HTTP"""
    
    def __init__(self):
        self.security_headers = {
            'Strict-Transport-Security': {
                'name': 'HSTS',
                'description': 'Força conexões HTTPS',
                'risk_level': 'high'
            },
            'Content-Security-Policy': {
                'name': 'CSP',
                'description': 'Previne ataques XSS',
                'risk_level': 'high'
            },
            'X-Frame-Options': {
                'name': 'Clickjacking Protection',
                'description': 'Previne ataques de clickjacking',
                'risk_level': 'medium'
            },
            'X-Content-Type-Options': {
                'name': 'MIME Sniffing Protection',
                'description': 'Previne MIME sniffing',
                'risk_level': 'medium'
            },
            'Referrer-Policy': {
                'name': 'Referrer Policy',
                'description': 'Controla informações de referrer',
                'risk_level': 'low'
            },
            'X-XSS-Protection': {
                'name': 'XSS Protection',
                'description': 'Proteção contra XSS (legacy)',
                'risk_level': 'low'
            }
        }
    
    def scan_headers(self, url: str) -> Dict[str, Any]:
        """Realiza scan dos cabeçalhos de segurança"""
        try:
            # Fazer requisição HTTP
            response = requests.get(url, timeout=10, verify=True)
            
            results = {
                'url': url,
                'status_code': response.status_code,
                'headers_found': {},
                'missing_headers': {},
                'security_score': 0,
                'recommendations': []
            }
            
            total_headers = len(self.security_headers)
            found_headers = 0
            
            # Verificar cada cabeçalho de segurança
            for header, info in self.security_headers.items():
                if header in response.headers:
                    results['headers_found'][header] = {
                        'value': response.headers[header],
                        'name': info['name'],
                        'description': info['description'],
                        'status': 'present'
                    }
                    found_headers += 1
                else:
                    results['missing_headers'][header] = {
                        'name': info['name'],
                        'description': info['description'],
                        'risk_level': info['risk_level'],
                        'status': 'missing'
                    }
                    
                    # Adicionar recomendação
                    results['recommendations'].append(
                        f"Implementar {info['name']}: {info['description']}"
                    )
            
            # Calcular score de segurança
            results['security_score'] = int((found_headers / total_headers) * 100)
            
            return results
            
        except requests.exceptions.RequestException as e:
            return {
                'url': url,
                'error': f"Erro ao acessar URL: {str(e)}",
                'status': 'failed'
            }
    
    def check_ssl_certificate(self, url: str) -> Dict[str, Any]:
        """Verifica informações do certificado SSL/TLS"""
        try:
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            port = parsed_url.port or 443
            
            # Conectar e obter certificado
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
            
            return {
                'hostname': hostname,
                'issuer': dict(x[0] for x in cert.get('issuer', [])),
                'subject': dict(x[0] for x in cert.get('subject', [])),
                'version': cert.get('version'),
                'serial_number': cert.get('serialNumber'),
                'not_before': cert.get('notBefore'),
                'not_after': cert.get('notAfter'),
                'signature_algorithm': cert.get('signatureAlgorithm'),
                'status': 'valid'
            }
            
        except Exception as e:
            return {
                'hostname': urlparse(url).hostname,
                'error': f"Erro ao verificar SSL: {str(e)}",
                'status': 'failed'
            }

# Função helper para usar o scanner
def scan_website_security(url: str) -> Dict[str, Any]:
    """Função principal para scan completo"""
    scanner = SecurityHeadersScanner()
    
    # Garantir que URL tenha protocolo
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Realizar scans
    headers_result = scanner.scan_headers(url)
    ssl_result = scanner.check_ssl_certificate(url)
    
    return {
        'url': url,
        'timestamp': str(requests.utils.datetime.datetime.now()),
        'headers_analysis': headers_result,
        'ssl_analysis': ssl_result,
        'overall_score': headers_result.get('security_score', 0)
    }