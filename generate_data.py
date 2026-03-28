import pandas as pd
import random
from datetime import datetime, timedelta

# Configuração
num_users = 150
conversao_rate = 0.03  # 3% de taxa de conversão
base_date = datetime(2024, 3, 20)

# Eventos do funil
funil = ['page_view', 'view_item', 'add_to_cart', 'begin_checkout', 'payment_info', 'purchase']

# Probabilidades de avanço no funil
prob_avanco = {
    'page_view': 1.0,           # Todos que entram
    'view_item': 0.75,          # 75% clicam em um produto
    'add_to_cart': 0.35,        # 35% adicionam ao carrinho
    'begin_checkout': 0.60,     # 60% dos que têm carrinho começam checkout
    'payment_info': 0.85,       # 85% continuam para pagamento
    'purchase': 0.3             # 3% de taxa final
}

# URLs do site
urls = {
    'page_view': 'https://loja.com.br/',
    'view_item': 'https://loja.com.br/produto/',
    'add_to_cart': 'https://loja.com.br/carrinho',
    'begin_checkout': 'https://loja.com.br/checkout',
    'payment_info': 'https://loja.com.br/pagamento',
    'purchase': 'https://loja.com.br/confirmacao'
}

# Preços dos produtos
precos_produtos = [29.90, 49.90, 79.90, 99.90, 149.90, 199.90, 299.90]

dados = []

for user_id in range(1, num_users + 1):
    user_key = f'user_{user_id:03d}'
    timestamp = base_date + timedelta(hours=random.randint(0, 168))
    
    for idx, evento in enumerate(funil):
        # Decidir se o usuário avança
        if random.random() < prob_avanco.get(evento, 1.0):
            # Adicionar variação ao timestamp
            event_time = timestamp + timedelta(minutes=random.randint(idx*5, (idx+1)*5))
            
            # Valor do evento
            if evento == 'view_item':
                valor = random.choice(precos_produtos)
            elif evento in ['add_to_cart', 'begin_checkout', 'payment_info']:
                valor = random.choice(precos_produtos)
            elif evento == 'purchase':
                valor = random.choice(precos_produtos) * random.uniform(0.9, 2.5)
            else:
                valor = 0
            
            url = urls[evento]
            
            dados.append({
                'event_name': evento,
                'timestamp': event_time.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id': user_key,
                'event_value': round(valor, 2),
                'page_url': url
            })
        else:
            # Usuário abandonou nesse ponto
            break

# Criar DataFrame e salvar
df = pd.DataFrame(dados)
df = df.sort_values('timestamp')

# Salvar CSV
output_file = 'examples/sample_data.csv'
df.to_csv(output_file, index=False)

print(f"✅ Arquivo criado: {output_file}")
print(f"📊 Estatísticas:")
print(f"   • Total de eventos: {len(df)}")
print(f"   • Usuários únicos: {df['user_id'].nunique()}")
conversoes = df[df['event_name'] == 'purchase']['user_id'].nunique()
taxa_conv = (conversoes / df['user_id'].nunique() * 100)
print(f"   • Taxa de conversão: {taxa_conv:.2f}%")
print(f"   • Valor médio da compra: R$ {df[df['event_name'] == 'purchase']['event_value'].mean():.2f}")
print(f"   • Data: {df['timestamp'].min()} até {df['timestamp'].max()}")
print(f"\n📋 Primeiros 10 eventos:")
print(df.head(10).to_string(index=False))
