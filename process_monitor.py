import subprocess
import time
import sys
import argparse

def run_process(command, output_file, timeout=None, restart_on_fail=False):
    start_time = time.time()
    with open(output_file, 'w') as f:
        while True:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            try:
                for line in process.stdout:
                    print(line, end='')
                    f.write(line)
                process.wait(timeout=timeout - (time.time() - start_time))
            except subprocess.TimeoutExpired:
                print("Процесс был принудительно остановлен по таймауту.")
                process.kill()
                break
            if process.returncode == 0 or not restart_on_fail:
                break
            print("Процесс упал, перезапускаю...")
            time.sleep(1)  # небольшая задержка перед перезапуском

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Мониторинг и управление процессами")
    parser.add_argument('command', nargs='+', help='Команда для запуска процесса')
    parser.add_argument('--output', '-o', required=True, help='Файл для записи вывода процесса')
    parser.add_argument('--timeout', '-t', type=int, help='Таймаут в секундах, после которого процесс будет убит')
    parser.add_argument('--restart', '-r', action='store_true', help='Перезапускать процесс, если он упал')
    
    args = parser.parse_args()

    run_process(args.command, args.output, args.timeout, args.restart)
