# Running code on a new machine

```
sudo apt-get install htop tmux python3-pip git
# if attempting to install matplotlib - disabled for now because too many issues
# sudo apt-get install libfreetype6-dev pkg-config
## libfreetype6-dev required for matplotlib
## pkg-config required as per https://github.com/matplotlib/matplotlib/issues/3029/

pip install -r friends-of-the-round-table/requirements.txt

python3 main.py GreedySwapper 20 # example code for running the GreedySwapper on a table of size 20
# add --info flag for information. process searches for checkpoint to restart from these checkpoints first.
# you may choose to (and probably should) run via tmux so you can disconnect without the process terminating.
```
