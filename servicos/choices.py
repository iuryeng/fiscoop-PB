UNIDADES = (
    ('Mês', 'Mês'),
    ('und', 'Unidade'),
    ('m²', 'Metro Quadrado'),
    ('m³', 'Metro Cúbico'),
    ('m', 'Metro'),
    ('kg', 'Kilograma'),
    ('T', 'Toneladas')
)


STATUS_CHOICES = (
    ('EXEC', 'Em Execução'),
    ('PARA', 'Paralisado'),
    ('NAO_INI', 'Não Iniciado'),
    ('CONCL', 'Concluído'),
)

TIPO_SERVICO_CISTERNA = (
    ('SERVICOS_PRELIMINARES', 'SERVIÇOS PRELIMINARES'),
    ('MOVIMENTO_TERRA', 'MOVIMENTO DE TERRA'),
    ('PAREDES', 'PAREDES'),
    ('ESTRUTURA', 'ESTRUTURA'),
    ('REVESTIMENTO', 'REVESTIMENTO'),
    ('INSTALACOES_HIDRAULICAS', 'INSTALAÇÕES HIDRÁULICAS'),
    ('PAVIMENTACAO', 'PAVIMENTAÇÃO'),
    ('PINTURA', 'PINTURA'),
    ('BOMBA_MANUAL', 'BOMBA MANUAL'),
    ('FILTRO_PRIMEIRAS_AGUAS', 'FILTRO DE PRIMEIRAS ÁGUAS'),
    ('SERVICOS_DIVERSOS', 'SERVIÇOS DIVERSOS'),
)


TIPO_SERVICO_PASSAGEM_MOLHADA = (
    ('SERVICOS_PRELIMINARES', 'SERVIÇOS PRELIMINARES'),
    ('TERRAPLENAGEM', 'TERRAPLENAGEM'),
    ('PASSAGEM_MOLHADA', 'PASSAGEM MOLHADA'),
)
