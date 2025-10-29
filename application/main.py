from collections import deque
from datetime import datetime

# -----------------------------
# Estruturas de dados
# -----------------------------
pacientes = []
medicos = []
exames = []
agendamentos = []
atendimentos = []
fila_atendimento = deque()


# -----------------------------
# Helpers básicos
# -----------------------------
def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def input_int_range(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = int(input(prompt))
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                print(f"Digite um número entre {min_val} e {max_val}.")
                continue
            return val
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def confirmar_acao(msg="Deseja continuar? (s/n): "):
    return input(msg).strip().lower() == 's'


# -----------------------------
# Passo 2: cadastro, estatísticas, busca, listar
# -----------------------------
def cadastrar_paciente():
    print("\n=== CADASTRAR PACIENTE ===")
    nome = input("Nome: ").strip()
    idade = input_int("Idade: ")
    telefone = input("Telefone: ").strip()
    cpf = input("CPF (opcional): ").strip()
    paciente = {"nome": nome, "idade": idade, "telefone": telefone, "cpf": cpf}
    pacientes.append(paciente)
    print("Paciente cadastrado com sucesso!")


def ver_estatisticas():
    print("\n=== ESTATÍSTICAS ===")
    if not pacientes:
        print("Nenhum paciente cadastrado.")
        return
    total = len(pacientes)
    soma = sum(p['idade'] for p in pacientes)
    media = soma / total
    mais_novo = min(pacientes, key=lambda p: p['idade'])
    mais_velho = max(pacientes, key=lambda p: p['idade'])
    print(f"Total de pacientes: {total}")
    print(f"Idade média: {media:.1f} anos")
    print(f"Mais novo: {mais_novo['nome']} ({mais_novo['idade']} anos)")
    print(f"Mais velho: {mais_velho['nome']} ({mais_velho['idade']} anos)")


def buscar_paciente():
    nome_busca = input("Digite nome (ou parte do nome): ").strip().lower()
    encontrados = [p for p in pacientes if nome_busca in p['nome'].lower()]
    if not encontrados:
        print("Nenhum paciente encontrado.")
        return
    for i, p in enumerate(encontrados, start=1):
        print(f"\n[{i}] Nome: {p['nome']}\nIdade: {p['idade']}\nTelefone: {p['telefone']}\nCPF: {p.get('cpf', '')}\n")


def listar_pacientes():
    if not pacientes:
        print("Nenhum paciente cadastrado.")
        return
    print("\n=== LISTA DE PACIENTES ===")
    for i, p in enumerate(pacientes, start=1):
        print(f"{i}. {p['nome']} | {p['idade']} anos | {p['telefone']} | CPF: {p.get('cpf', '')}")


# -----------------------------
# Cadastro simples de médicos/exames e agendamento
# -----------------------------
def cadastrar_medico():
    print("\n=== CADASTRAR MÉDICO ===")
    nome = input("Nome do médico: ").strip()
    esp = input("Especialidade: ").strip()
    medico_id = len(medicos) + 1
    medicos.append({'id': medico_id, 'nome': nome, 'especialidade': esp})
    print(f"Médico cadastrado com ID: {medico_id}")


def listar_medicos():
    if not medicos:
        print("Nenhum médico cadastrado.")
        return
    for m in medicos:
        print(f"ID {m['id']} - {m['nome']} ({m['especialidade']})")


def agendar_consulta():
    print("\n=== AGENDAR CONSULTA ===")
    if not pacientes or not medicos:
        print("É necessário ter pelo menos 1 paciente e 1 médico cadastrados.")
        return
    listar_pacientes()
    idx = input_int_range(f"Escolha o número do paciente (1-{len(pacientes)}): ", 1, len(pacientes)) - 1
    listar_medicos()
    mid = input_int_range(f"Digite ID do médico (1-{len(medicos)}): ", 1, len(medicos))
    m = next((x for x in medicos if x['id'] == mid), None)
    if not m:
        print("Médico inválido.")
        return
    data_str = input("Data e hora (YYYY-MM-DD HH:MM): ").strip()
    try:
        dh = datetime.strptime(data_str, "%Y-%m-%d %H:%M")
    except Exception:
        print("Formato inválido.")
        return
    conflito = any(a['medico_id'] == mid and a['datahora'] == dh for a in agendamentos)
    if conflito:
        print("Horário indisponível para esse médico.")
        return
    agendamentos.append({
        'paciente': pacientes[idx]['nome'],
        'medico_id': mid,
        'datahora': dh,
        'tipo': 'consulta'
    })
    print("Consulta agendada com sucesso.")


def listar_agendamentos():
    if not agendamentos:
        print("Nenhum agendamento.")
        return
    for a in agendamentos:
        med = next((m for m in medicos if m['id'] == a['medico_id']), {'nome': '--'})
        print(
            f"{a['datahora'].strftime('%Y-%m-%d %H:%M')} - {a['tipo']} - Paciente: {a['paciente']} - Médico: {med['nome']}")


# -----------------------------
# Registro de atendimentos (histórico)
# -----------------------------
def registrar_atendimento():
    print("\n=== REGISTRAR ATENDIMENTO ===")
    if not pacientes or not medicos:
        print("Cadastre pacientes e médicos primeiro.")
        return
    nome = input("Nome do paciente atendido: ").strip()
    paciente = next((p for p in pacientes if p['nome'].lower() == nome.lower()), None)
    if not paciente:
        print("Paciente não cadastrado.")
        return
    listar_medicos()
    mid = input_int_range(f"Digite ID do médico que atendeu (1-{len(medicos)}): ", 1, len(medicos))
    dh = datetime.now()
    obs = input("Observações: ").strip()
    atendimentos.append({
        'paciente': paciente['nome'],
        'medico_id': mid,
        'datahora': dh,
        'observacao': obs
    })
    print("Atendimento registrado.")


def ver_historico_paciente():
    nome = input("Nome do paciente para ver histórico: ").strip()
    hist = [a for a in atendimentos if a['paciente'].lower() == nome.lower()]
    if not hist:
        nomes_sugestao = [p['nome'] for p in pacientes if nome.lower() in p['nome'].lower()]
        if nomes_sugestao:
            print(f"Nenhum atendimento exato encontrado. Talvez você quis: {', '.join(nomes_sugestao)}")
        else:
            print("Nenhum atendimento registrado para esse paciente.")
        return
    for h in hist:
        med = next((m for m in medicos if m['id'] == h['medico_id']), {'nome': '--'})
        print(f"{h['datahora']} - Médico: {med['nome']} - Obs: {h['observacao']}")


# -----------------------------
# Relatório mensal simples
# -----------------------------
def gerar_relatorio_mes(ano, mes):
    print(f"\n=== RELATÓRIO {ano}-{mes:02d} ===")
    regs = [a for a in atendimentos if a['datahora'].year == ano and a['datahora'].month == mes]
    print(f"Total de atendimentos no mês: {len(regs)}")
    cont_med = {}
    for r in regs:
        cont_med[r['medico_id']] = cont_med.get(r['medico_id'], 0) + 1
    for mid, c in cont_med.items():
        med = next((m for m in medicos if m['id'] == mid), {'nome': '--'})
        print(f"Médico {med['nome']} (ID {mid}): {c} atendimentos")


# -----------------------------
# Controle de acesso
# -----------------------------
def acesso_consulta_normal(A, B, C, D):
    return (A and B and C) or (B and C and D)


def acesso_emergencia(A, B, C, D):
    return C and (B or D)


def testar_acesso_interativo():
    print("\n=== TESTE DE CONTROLE DE ACESSO ===")
    A = input("Paciente tem agendamento? (s/n): ").strip().lower() == 's'
    B = input("Documentos em dia? (s/n): ").strip().lower() == 's'
    C = input("Médico disponível? (s/n): ").strip().lower() == 's'
    D = input("Pagamentos em dia? (s/n): ").strip().lower() == 's'
    print("Consulta normal:", "Atendido" if acesso_consulta_normal(A, B, C, D) else "Negado")
    print("Emergência:", "Atendido" if acesso_emergencia(A, B, C, D) else "Negado")


# -----------------------------
# Fila FIFO
# -----------------------------
def pseudocodigo_fila():
    print("""
PSEUDOCÓDIGO (fila FIFO)
1. Criar fila vazia
2. Inserir 3 pacientes na fila (nome, CPF)
   - Enqueue(paciente1)
   - Enqueue(paciente2)
   - Enqueue(paciente3)
3. Remover o primeiro da fila para atendimento
   - atendimento = Dequeue()
4. Exibir quem ainda está na fila
   - Enquanto fila não vazia:
       mostrar elemento atual
""")


def inserir_3_pacientes_fila():
    print("\nInserir 3 pacientes na fila:")
    for i in range(3):
        nome = input(f"Nome do paciente {i + 1}: ").strip()
        cpf = input("CPF: ").strip()
        fila_atendimento.append({'nome': nome, 'cpf': cpf})
    print("3 pacientes inseridos na fila.")


def atender_primeiro_da_fila():
    if not fila_atendimento:
        print("Fila vazia.")
        return
    primeiro = fila_atendimento.popleft()
    print(f"Atendendo primeiro da fila: {primeiro['nome']} (CPF {primeiro['cpf']})")


def mostrar_fila():
    if not fila_atendimento:
        print("Fila vazia.")
        return
    print("Pacientes ainda na fila:")
    for i, p in enumerate(fila_atendimento, start=1):
        print(f"{i}. {p['nome']} - CPF: {p['cpf']}")


# -----------------------------
# Menu principal
# -----------------------------
def menu():
    while True:
        print("\n=== SISTEMA CLÍNICA VIDA+ ===")
        print("1. Cadastrar paciente")
        print("2. Ver estatísticas")
        print("3. Buscar paciente")
        print("4. Listar todos os pacientes")
        print("5. Cadastrar médico")
        print("6. Agendar consulta")
        print("7. Listar agendamentos")
        print("8. Registrar atendimento")
        print("9. Ver histórico de paciente")
        print("10. Gerar relatório mensal")
        print("11. Testar controle de acesso")
        print("12. Inserir 3 pacientes na fila")
        print("13. Atender primeiro da fila")
        print("14. Mostrar fila")
        print("15. Mostrar pseudocódigo da fila")
        print("0. Sair")

        opc = input_int_range("Escolha uma opção: ", 0, 15)
        if opc == 1:
            cadastrar_paciente()
        elif opc == 2:
            ver_estatisticas()
        elif opc == 3:
            buscar_paciente()
        elif opc == 4:
            listar_pacientes()
        elif opc == 5:
            cadastrar_medico()
        elif opc == 6:
            agendar_consulta()
        elif opc == 7:
            listar_agendamentos()
        elif opc == 8:
            registrar_atendimento()
        elif opc == 9:
            ver_historico_paciente()
        elif opc == 10:
            ano = input_int("Ano (ex: 2025): ")
            mes = input_int_range("Mês (1-12): ", 1, 12)
            gerar_relatorio_mes(ano, mes)
        elif opc == 11:
            testar_acesso_interativo()
        elif opc == 12:
            inserir_3_pacientes_fila()
        elif opc == 13:
            atender_primeiro_da_fila()
        elif opc == 14:
            mostrar_fila()
        elif opc == 15:
            pseudocodigo_fila()
        elif opc == 0:
            print("Saindo... Até logo.")
            break


if __name__ == "__main__":
    menu()
