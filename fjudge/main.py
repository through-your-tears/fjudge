import os
import re
import threading
import time
# import psutil
from abc import ABC, abstractmethod
from typing import List, Union
from subprocess import *


def run_process_with_mem_stop(process, mem):
    process = psutil.Process(process.pid)
    while process.poll() is None:
        if process.memory_info() / 1024 > mem:
            process.kill()
            return
        elif process.poll():
            return


def run_process_with_timeout(process, timeout_sec):
    start_time = time.time()
    poll = process.poll()
    while poll is None:
        if time.time() - start_time > timeout_sec:
            process.kill()
            return
        elif poll is not None:
            return


def noasm(file: str): # скорее всего не нужно
    with open(file, 'r'):
        return re.search(r'asm(.*)', file)


def get_data(data_path: str) -> List[List[bytes]]:
    data = []
    with open(data_path, 'r') as lines:
        s = []
        for line in lines:
            if line.strip() != '':
                s.append(bytes(line, encoding='utf8'))
            else:
                data.append(s)
                s = []
        data.append(s)
    return data


""""Эталон работы на данный момент(почти, починить скрипт, который всегда false"""


def isSolvedC(test_path, student_path, tests, max_time, max_size, answers_path, script=False):
    inputs = get_data(tests)
    i = 1
    if script:
        # тут правильно вылетает на времени
        for inp in inputs:
            test = Popen(["python", test_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            student = Popen(student_path, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            out1 += b'\r\n'
            if err:
                return str(err.strip().decode())
            elif out1 != out2:
                return f'Неправильный ответ на {i} тесте'
            student.terminate()
            test.terminate()
            i += 1
    else:
        answers = get_data(answers_path)
        for inp in inputs:
            student = Popen(student_path, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            time_thread = threading.Thread(target=run_process_with_timeout, args=(student, max_time))
            time_thread.start()
            mem_thread = threading.Thread(target=run_process_with_mem_stop, args=(student, max_size))
            mem_thread.start()
            for j in inp:
                student.stdin.write(bytes(j, encoding='utf-8'))
            student.stdin.close()
            err = student.stderr.read()
            if student.poll() is None:
                return f'Превышено ограничение по времени на тесте {i}'
            out1 = student.stdout.read()
            out1 += b'\n'
            out2 = ''.join(answers[i - 1]).encode('utf-8')
            if err:
                return str(err.strip().decode())
            elif out1 != out2:
                return f'Неправильный ответ на {i} тесте'
            student.terminate()
            i += 1
    return 'OK'


def isSolvedJava(test_path, student_path, tests, max_time, max_size, answers_path, script=False):
    inputs = get_data(tests)
    s = student_path[::-1].replace('/', ' /', 1)
    student_path = s[::-1]
    i = 1
    if script:
        for inp in inputs:
            test = Popen(["python", test_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            student = Popen(f"java -cp {student_path}", stdin=PIPE, stdout=PIPE, stderr=PIPE)
            try:
                # signal = Alarm(max_time)
                # signal.start()
                for j in inp:
                    student.stdin.write(bytes(j, encoding='utf-8'))
                student.stdin.close()
                # del signal
            except TimeoutError:
                return f'Превышено ограничение по времени на тесте {i}'
            for j in inp:
                test.stdin.write(bytes(j, encoding='utf-8'))
            test.stdin.close()
            err = student.stderr.read()
            out1 = student.stdout.read()
            out2 = test.stdout.read()
            out1 += b'\r\n'
            if err:
                return str(err.strip().decode())
            elif out1 != out2:
                return f'Неправильный ответ на {i} тесте'
            i += 1
    else:
        answers = get_data(answers_path)
        for inp in inputs:
            student = Popen(f"java -cp {student_path}", stdin=PIPE, stdout=PIPE, stderr=PIPE)
            try:
                # signal = Alarm(max_time)
                # signal.start()
                for j in inp:
                    student.stdin.write(bytes(j, encoding='utf-8'))
                student.stdin.close()
                # del signal
            except TimeoutError:
                return f'Превышено ограничение по времени на тесте {i}'
            err = student.stderr.read()
            out1 = student.stdout.read()
            out1 += b'\n'
            out2 = ''.join(answers[i - 1]).encode('utf-8')
            if err:
                return str(err.strip().decode())
            elif out1 != out2:
                return f'Неправильный ответ на {i} тесте'
            i += 1
    return 'OK'


def isSolvedPy(test_path, student_path, tests, max_time, max_size, answers_path, script=False):
    inputs = get_data(tests)
    i = 1
    if script:
        for inp in inputs:
            test = Popen(["python", test_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            try:
                student = Popen(['python', student_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            except Exception:
                return 'Ошибка компиляции'
            time_thread = threading.Thread(target=run_process_with_timeout, args=(student, max_time))
            time_thread.start()
            mem_thread = threading.Thread(target=run_process_with_mem_stop, args=(student, max_size))
            mem_thread.start()
            os.getpid()
            for j in inp:
                student.stdin.write(bytes(j, encoding='utf-8'))
            student.stdin.close()
            for j in inp:
                test.stdin.write(bytes(j, encoding='utf-8'))
            test.stdin.close()
            err = student.stderr.read()
            if student.poll() is None:
                return f'Превышено ограничение по времени на тесте {i}'
            out1 = student.stdout.read()
            out2 = test.stdout.read()
            if err:
                return str(err.strip().decode())
            elif out1 != out2:
                return f'Неправильный ответ на {i} тесте'
            i += 1

    return 'OK'


# def main(path, max_time, max_size, script):
#     answers_path = '../answers.txt'
#     tests_path = '../tests.txt'
#     test_path = '../test.py'
#     filename, file_extension = os.path.splitext(path)
#     if isinstance(file_extension, str):
#         if file_extension == '.cpp':
#             if noasm(path):
#                 print('Ассемблерная вставка')
#                 return
#             else:
#                 new_path = path.replace(file_extension, '.exe')
#                 try:
#                     run(f'g++ -o {new_path} {path}', check=True)
#                 except CalledProcessError:
#                     return 'compile error'
#                 return isSolvedC(test_path, new_path, tests_path, max_time, max_size, answers_path, script)
#         elif file_extension == '.java':
#             try:
#                 run(f'javac {path}', check=True)
#             except CalledProcessError:
#                 return 'compile error'
#             return isSolvedJava(test_path, filename, tests_path, max_time, max_size, answers_path, script)
#         elif file_extension == '.c':
#             new_path = path.replace(file_extension, '.exe')
#             try:
#                 run(f'gcc -o {new_path} {path}', check=True)
#             except CalledProcessError:
#                 return 'compile error'
#             return isSolvedC(test_path, new_path, tests_path, max_time, max_size, answers_path, script)
#         elif file_extension == '.py':
#             return isSolvedPy(test_path, path, tests_path, max_time, max_size, answers_path, script)


compiling_languages = {
    'java': lambda path: f'javac {path}',
    'cpp': lambda path: f'g++ {path}',
}

compiling_languages_filepath = {
    'java': lambda path: path,
    'cpp': lambda path: path.replace('cpp', '.exe')
}

building_commands = {
    'python': lambda path: f'docker build -f {path} -d'
}

launch_commands = {
    'java': lambda path: f"java -cp {path}",
    'cpp': lambda path: path,
    'python': lambda path, memory, time: f'docker run -e filepath={path} -m={memory}m --stop-timeout={time} '
}


class Program:

    def __init__(self, filepath: str, language: str):
        self.filepath = filepath if filepath not in compiling_languages.keys() else Program.compile(filepath, language)
        self.language = language
        self.pid = None

    @staticmethod
    def compile(filepath: str, language: str) -> str:
        compiling_languages[language](filepath)
        return compiling_languages_filepath[language](filepath)

    def build_container(self):
        process = run(building_commands['python'](self.filepath), stdout=PIPE)
        self.pid = process.stdout

    def launch(self, input: List[bytes]) -> List[bytes]:
        program = Popen(f'docker exec -it {self.pid} {launch_commands[self.language]}', stdin=PIPE, stdout=PIPE, stderr=PIPE)
        program.stdin.writelines(input)
        err = program.stderr.read()
        if err:
            raise Exception(str(err))
        return program.stdout.readlines()

    def destroy_container(self):
        run(f'docker rm -v {self.pid}')


class Judge(ABC):

    def __init__(self, student: Program, tester: Union[Program, str], inputs: str, memory_limit: float,
                 time_limit: float):
        self.student: Program = student
        self.tester: Union[Program, str] = tester
        self.memory_limit: float = memory_limit
        self.time_limit: float = time_limit
        self.inputs: List[List[bytes]] = get_data(inputs)

    @abstractmethod
    def prove(self) -> str:
        pass


class FileJudge(Judge):

    def prove(self):
        i: int = 0
        tester_results = get_data(self.tester)
        for input in self.inputs:
            try:
                student_result = self.student.launch(input)
            except Exception as e: # продумай норм исключение
                return str(e)
            for j in range(len(tester_results[i])):
                if student_result[j] != tester_results[i][j]:
                    return f'Неправильный ответ на {i+1} тесте'
            i += 1
        self.student.destroy_container()
        return "OK"


class ProgramJudge(Judge):

    def prove(self):
        pass


class CheckerJudge(Judge):

    def prove(self):
        pass


st = Program('../test.py', 'python')
judge = FileJudge(st, '../answers.txt', '../tests.txt', 200, 2)
print(judge.prove())
