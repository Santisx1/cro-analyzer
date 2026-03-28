#!/usr/bin/env python3
"""
Debug e Monitor do CRO Scheduler
Ferramenta para verificar status, logs e executar análises manuais
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

# Cores
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

PROJECT_DIR = Path("/Users/kaiofernandes/Desktop/Análise de CRO")
REPORTS_DIR = PROJECT_DIR / "reports_automated"
LOG_FILE = PROJECT_DIR / "scheduler.log"
LAUNCHD_LOG = PROJECT_DIR / "launchd.log"
LAUNCHD_ERROR_LOG = PROJECT_DIR / "launchd_error.log"

def print_header(text: str) -> None:
    """Print colored header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}{Colors.RESET}\n")

def check_environment() -> bool:
    """Verificar ambiente"""
    print_header("Verificando Ambiente")
    
    checks = {
        "✓ Projeto existe": PROJECT_DIR.exists(),
        "✓ Python venv existe": (PROJECT_DIR / "venv").exists(),
        "✓ scheduler.py existe": (PROJECT_DIR / "scheduler.py").exists(),
        "✓ requirements.txt existe": (PROJECT_DIR / "requirements.txt").exists(),
        "✓ Diretório reports_automated": REPORTS_DIR.exists(),
    }
    
    all_ok = True
    for check, result in checks.items():
        status = f"{Colors.GREEN}OK{Colors.RESET}" if result else f"{Colors.RED}FALHA{Colors.RESET}"
        print(f"  {check}: {status}")
        if not result:
            all_ok = False
    
    return all_ok

def check_scheduler_process() -> bool:
    """Verificar se scheduler está rodando"""
    print_header("Status do Scheduler")
    
    try:
        result = subprocess.run(
            ["pgrep", "-f", "scheduler.py"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            pid = result.stdout.strip()
            print(f"  {Colors.GREEN}✓ Scheduler EM EXECUÇÃO{Colors.RESET}")
            print(f"  PID: {pid}")
            return True
        else:
            print(f"  {Colors.YELLOW}✗ Scheduler NÃO está rodando{Colors.RESET}")
            return False
    except Exception as e:
        print(f"  {Colors.RED}Erro ao verificar: {e}{Colors.RESET}")
        return False

def check_launchd_status() -> Optional[str]:
    """Verificar status do LaunchD"""
    print_header("Status LaunchD (macOS)")
    
    try:
        result = subprocess.run(
            ["launchctl", "list"],
            capture_output=True,
            text=True
        )
        
        if "com.cro.analyzer.scheduler" in result.stdout:
            print(f"  {Colors.GREEN}✓ LaunchD Agent INSTALADO{Colors.RESET}")
            
            # Tentar obter mais detalhes
            for line in result.stdout.split('\n'):
                if "com.cro.analyzer.scheduler" in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        status_code = parts[0]
                        print(f"  Status: {status_code}")
                        if status_code == "-":
                            print(f"    (Significa: Não está em execução no momento)")
                        break
            return "installed"
        else:
            print(f"  {Colors.YELLOW}✗ LaunchD Agent NÃO instalado{Colors.RESET}")
            print(f"  Para instalar: ./setup_launchd.sh")
            return "not_installed"
    except FileNotFoundError:
        print(f"  {Colors.RED}launchctl não encontrado (não é Mac?)${Colors.RESET}")
        return None
    except Exception as e:
        print(f"  {Colors.RED}Erro: {e}{Colors.RESET}")
        return None

def show_recent_reports(limit: int = 5) -> None:
    """Mostrar relatórios recentes"""
    print_header(f"Últimos {limit} Relatórios")
    
    if not REPORTS_DIR.exists():
        print(f"  {Colors.YELLOW}Diretório vazio (primeira execução)${Colors.RESET}")
        return
    
    html_files = sorted(
        REPORTS_DIR.glob("*.html"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )[:limit]
    
    if not html_files:
        print(f"  {Colors.YELLOW}Nenhum relatório encontrado${Colors.RESET}")
        return
    
    for f in html_files:
        size_kb = f.stat().st_size / 1024
        mod_time = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        print(f"  {f.name}")
        print(f"    Tamanho: {size_kb:.1f} KB")
        print(f"    Modificado: {mod_time}")
        print()

def show_logs(filename: Path, lines: int = 20) -> None:
    """Mostrar últimas linhas de log"""
    if not filename.exists():
        print(f"  {Colors.YELLOW}Arquivo não encontrado${Colors.RESET}")
        return
    
    try:
        with open(filename) as f:
            all_lines = f.readlines()
            recent = all_lines[-lines:] if len(all_lines) > lines else all_lines
            
        for line in recent:
            print(f"  {line.rstrip()}")
    except Exception as e:
        print(f"  {Colors.RED}Erro ao ler: {e}${Colors.RESET}")

def show_scheduler_logs() -> None:
    """Mostrar logs do scheduler"""
    print_header(f"Logs do Scheduler (últimas 20 linhas)")
    show_logs(LOG_FILE, 20)

def show_launchd_logs() -> None:
    """Mostrar logs do LaunchD"""
    print_header(f"Logs LaunchD - Output (últimas 20 linhas)")
    show_logs(LAUNCHD_LOG, 20)
    
    print_header(f"Logs LaunchD - Erros (últimas 20 linhas)")
    show_logs(LAUNCHD_ERROR_LOG, 20)

def run_analysis() -> None:
    """Rodar análise manual"""
    print_header("Executando Análise Manual")
    
    python_exe = PROJECT_DIR / "venv" / "bin" / "python3"
    
    if not python_exe.exists():
        print(f"  {Colors.RED}Python venv não encontrado${Colors.RESET}")
        return
    
    try:
        print(f"  Iniciando análise...")
        result = subprocess.run(
            [str(python_exe), str(PROJECT_DIR / "scheduler.py"), "--run"],
            cwd=str(PROJECT_DIR),
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print(f"  {Colors.GREEN}✓ Análise concluída com sucesso!${Colors.RESET}")
            print(f"\n  Output:\n{result.stdout}")
        else:
            print(f"  {Colors.RED}✗ Erro na execução${Colors.RESET}")
            print(f"\n  Erro:\n{result.stderr}")
    except subprocess.TimeoutExpired:
        print(f"  {Colors.RED}✗ Análise timeout (> 5 minutos)${Colors.RESET}")
    except Exception as e:
        print(f"  {Colors.RED}Erro: {e}${Colors.RESET}")

def show_stats() -> None:
    """Mostrar estatísticas"""
    print_header("Estatísticas")
    
    if not REPORTS_DIR.exists():
        print(f"  {Colors.YELLOW}Nenhum relatório gerado ainda${Colors.RESET}")
        return
    
    html_files = list(REPORTS_DIR.glob("*.html"))
    json_files = list(REPORTS_DIR.glob("*.json"))
    
    total_size = sum(f.stat().st_size for f in html_files + json_files) / (1024 * 1024)
    
    print(f"  Relatórios HTML: {len(html_files)}")
    print(f"  Arquivos JSON: {len(json_files)}")
    print(f"  Espaço total: {total_size:.2f} MB")
    
    if html_files:
        oldest = min(html_files, key=lambda x: x.stat().st_mtime)
        newest = max(html_files, key=lambda x: x.stat().st_mtime)
        
        oldest_time = datetime.fromtimestamp(oldest.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        newest_time = datetime.fromtimestamp(newest.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n  Primeiro relatório: {oldest_time}")
        print(f"  Último relatório: {newest_time}")

def main_menu() -> None:
    """Menu principal"""
    while True:
        print(f"\n{Colors.BLUE}{Colors.BOLD}CRO Scheduler - Debug & Monitor{Colors.RESET}\n")
        
        print("Opções:")
        print("  1. Verificar ambiente completo")
        print("  2. Ver status do scheduler")
        print("  3. Ver status LaunchD")
        print("  4. Ver logs do scheduler")
        print("  5. Ver logs LaunchD")
        print("  6. Ver últimos relatórios")
        print("  7. Ver estatísticas")
        print("  8. Rodar análise manual")
        print("  9. SAIR")
        print()
        
        choice = input("Escolha (1-9): ").strip()
        
        if choice == "1":
            check_environment()
            check_scheduler_process()
            check_launchd_status()
            check_scheduler_process()
            show_stats()
            input("\nPressione ENTER para continuar...")
        
        elif choice == "2":
            check_scheduler_process()
            input("\nPressione ENTER para continuar...")
        
        elif choice == "3":
            check_launchd_status()
            input("\nPressione ENTER para continuar...")
        
        elif choice == "4":
            show_scheduler_logs()
            input("\nPressione ENTER para continuar...")
        
        elif choice == "5":
            show_launchd_logs()
            input("\nPressione ENTER para continuar...")
        
        elif choice == "6":
            show_recent_reports(10)
            input("\nPressione ENTER para continuar...")
        
        elif choice == "7":
            show_stats()
            input("\nPressione ENTER para continuar...")
        
        elif choice == "8":
            run_analysis()
            input("\nPressione ENTER para continuar...")
        
        elif choice == "9":
            print("\nAté logo! 👋\n")
            break
        
        else:
            print(f"{Colors.RED}Opção inválida${Colors.RESET}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Modo comando
        if sys.argv[1] == "--check":
            check_environment()
            check_scheduler_process()
            check_launchd_status()
            show_stats()
        elif sys.argv[1] == "--run":
            run_analysis()
        elif sys.argv[1] == "--logs":
            show_scheduler_logs()
        else:
            print(f"Opção desconhecida: {sys.argv[1]}")
    else:
        # Menu interativo
        try:
            main_menu()
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Interrompido pelo usuário${Colors.RESET}\n")
            sys.exit(0)
