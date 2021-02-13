import time
from pathlib import Path
import sys, os

from discopusher import Config, Hook, push

def safe_mkdir(*args):
    for path in args:
        path.mkdir(parents=True, exist_ok=True)

def handle_cli(hooks):
    if 'webhook' in os.environ:
        webhooks = [os.environ['webhook']]
    else:
        webhooks = [webhook for webhooks in [hook.config.get('webhooks') for hook in filter(lambda x: x.type == 'cli', hooks)]]
    options = {
        'avatar_url': os.environ.get('webhook_avatar'),
        'username': os.environ.get('webhook_username')
    }
    for path in sys.argv[1:]:
        with open(path) as f:
            content = f.read()
            for webhook in webhooks:
                push(content, webhook, options)

def main():
    config = Config('config.toml', write_defaults=True, defaults={
        'handlers_config_dir': '.',
        'hooks_dir': './hooks',
        'data_dir': './data',
    })
    config.save()
    hooks_dir = Path(config['hooks_dir'])
    data_dir = Path(config['data_dir'])
    safe_mkdir(hooks_dir, data_dir)
    hooks = [Hook(path, app_config=config) for path in hooks_dir.glob('*.toml')]
    if len(sys.argv) > 1:
        handle_cli(hooks)
        return
    for hook in hooks:
        hook.handle()
        time.sleep(.2)

try:
    main()
except ModuleNotFoundError as e:
    modules_tr = {
        'twitter': 'python-twitter'
    }
    module_not_found = str(e).split('\'')[1]
    tr_module = modules_tr.get(module_not_found, module_not_found)
    msg = (
        'Module "{0}" could not be found.'
        '\nMake sure you ran  pip install -r requirements.txt , possibly in a'
        ' virtual environment.'
        '\nOr manually install it by running  pip install {1} .'
    )
    print(msg.format(module_not_found, tr_module))
