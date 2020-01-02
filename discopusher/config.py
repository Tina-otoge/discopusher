from pathlib import Path

import toml

class Config:
    def __init__(self, path, defaults={}, write_defaults=False):
        self.path = Path(path)
        self.defaults = defaults
        self.write_defaults = write_defaults
        if not Path(path).is_file():
            self.data = {}
        else:
            with open(self.path, 'r') as f:
                self.data = toml.load(f, _dict=dict)

    def save(self):
        self.path.parent.mkdir(exist_ok=True)
        if self.write_defaults:
            tmp = self.defaults
            tmp.update(self.data)
            self.data = tmp
        with open(self.path, 'w') as f:
            toml.dump(self.data, f)

    def get(self, name, default=None):
        value = self[name]
        if value is None:
            return default
        return value

    def __getitem__(self, name):
        return self.data.get(name, self.defaults.get(name))

    def __setitem__(self, name, value):
        self.data[name] = value
        self.save()

    def __delitem__(self, name):
        self.data.pop(name)
        self.save()
