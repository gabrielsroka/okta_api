import json

from requests import Response
from typing import Any


def parse_safe_json_response(response: Response):
    return json.loads(response.text.replace('while(1){};', ''))


def print_progress_bar(iteration: int, total: int, prefix: str = 'Progress', suffix: str = 'Complete', decimals: int = 1, length: int = 100, fill: str = '█', printEnd: str = '\r'):
    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)

    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    
    # Print New Line on Complete
    if iteration == total: 
        print('\n\n')
