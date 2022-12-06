## adventofcode
my code for https://adventofcode.com/

## one-off steps to initialize the python environment (macos)

### install pyenv & pyenv-virtualenv

see https://realpython.com/intro-to-pyenv/#virtual-environments-and-pyenv

```
brew install pyenv pyenv-virtualenv
```

### add the following lines to your shell scripts

`~/.bashrc` (for bash), `~/.zprofile` and/or `~/.zshrc` (for zsh)

```
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

### install required python version
```
pyenv install 3.11
```

### create virtualenv in 2022
```
cd ./2022/
pyenv virtualenv 3.11 adventofcode2022
```


### activate virtualenv
```
pyenv local adventofcode2022
```

### upgrade pip and install deps
```
pip install --upgrade pip
pip install -r requirements.txt
```