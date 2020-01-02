from pathlib import Path

from discopusher import Config, Hook

def safe_mkdir(*args):
    for path in args:
        path.mkdir(parents=True, exist_ok=True)

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
    for path in hooks_dir.glob('*.toml'):
        hook = Hook(path, app_config=config)
        hook.handle()

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
