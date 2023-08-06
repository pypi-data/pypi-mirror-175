# WalletBoy

## Crypto wallet application

Supported exchanges: COINBASE

### Installing

```
git clone https://github.com/TraylorBoy/WalletBoy.git
```

or

```
pip install walletboy
```

## Usage

Store key, secret, and passphrase (if applicable) into a **.env** file

```
API_KEY=""
SECRET=""
PASSPHRASE=""
```

Connect to one of the supported exchanges

```
from walletboy import WalletBoy

wallet = WalletBoy('coinbase')
```

Get the price of an exchange pair

```
print(wallet.get_price('BTC-USD'))
print(wallet.get_price('ETH-USD'))

> 20705.85
> 1584.44
```

Get the balances of all tokens currently in exchange wallet greater than 0
including the USD value of each pairing

```
print(wallet.get_balances())

> [{'currency': 'ADA', 'balance': Decimal('0.029958'), 'USD': Decimal('0.01')}, {'currency': 'ALGO', 'balance': Decimal('0.718314'), 'USD': Decimal('0.31')}, {'currency': 'BTC', 'balance': Decimal('0.000014'), 'USD': Decimal('0.29')}, {'currency': 'DAI', 'balance': Decimal('0.018596'), 'USD': Decimal('0.02')}, {'currency': 'DOGE', 'balance': Decimal('0.020000'), 'USD': Decimal('0.00')}, {'currency': 'USD', 'balance': Decimal('0.062499'), 'USD': Decimal('0.06')}, {'currency': 'USDC', 'balance': Decimal('0.000048'), 'USD': Decimal('0.00')}, {'currency': 'XLM', 'balance': Decimal('0.287762'), 'USD': Decimal('0.03')}, {'currency': 'XTZ', 'balance': Decimal('0.010000'), 'USD': Decimal('0.01')}, {'currency': 'ZEC', 'balance': Decimal('0.000024'), 'USD': Decimal('0.00')}]
```

Get the total of all balances currently in wallet in USD

```
print(wallet.get_total())

> 0.73
```

## Test

```
make test
```
