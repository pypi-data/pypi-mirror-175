# Fancy BTC Price

Simple program that shows the BTC price taken from the Money on Chain API Rest



## Refrences

* [Source code in Github](https://github.com/jbokser/fancy_btc_price)
* [Package from Python package index (PyPI)](https://pypi.org/project/fancy-btc-price)
* [Money on Chain](https://moneyonchain.com)



## Requirements

* Python 3.6+



## Installation

### From the Python package index (PyPI)

Run:

```
$ pip3 install fancy-btc-price
```

### From source

Download from [Github](https://github.com/jbokser/fancy_btc_price)

Standing inside the folder, run:

```
$ pip3 install -r requirements.txt
```

For install the dependencies and then run:

```
$ pip3 install .
```



## Run

```
user@host:~$ fancy_btc_price
1₿=21685$
user@host:~$
```

More options

```
user@host:~$ fancy_btc_price --help
Usage: fancy_btc_price [OPTIONS]

  Simple program that shows the BTC price

  Taken from the Money on Chain API Rest (moneyonchain.com)

Options:
  -v, --verbose                Enables verbose mode
  --version                    Show version and exit
  -m, --max-age INTEGER RANGE  Max price age without showing a warning (in
                               minutes)  [default: 3; 1<=x<=120]
  --help                       Show this message and exit.
user@host:~$
```
