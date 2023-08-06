# BotBoy
Multithreading &amp; processing worker that executes functions and prints the
result

## Installation
```
pip install botboy
```

## Usage
### Create a new BotBoy object with a pre-defined function object and a name

```
from botboy import BotBoy

bot = BotBoy('Adder', lambda x, y: x + y)
```

### Display the information

```
bot.display_information()

> Adder
> <function <lambda> at 0x10e6e8040>
```

### Set new task to run

```
bot.set_task(lambda x, y: x - y)
```

### Execute function object on separate thread

```
bot.execute(1, 2)

> Adder is executing task: <function <lambda> at 0x10e6e8040>
> Retrieved result from Adder: 3
```

### Execute function object on separate process

```
bot.set_processing() # Can be turned back to thread by running same method

bot.execute(3, 4)

> Adder is executing task: <function <lambda> at 0x10e6e8040>
> Retrieved result from Adder: 7
```

### Store result in file *result.txt*

```
bot.set_on_file() # Can be turned back to off by running same method

bot.execute(7, 8)

> Adder is executing task: <function <lambda> at 0x10a1e2040>
> Retrieved result from Adder: 15
> Storing result in file: result.txt
```

### Pause execution for threads and wait for result

```
bot.set_wait() # Can be turned back to off by running same method

bot.execute(100, 10000)

> Waiting for <function <lambda> at 0x109f023b0> to finish
> Adder is executing task: <function <lambda> at 0x109f023b0>
> Retrieved result from Adder: 10100
```

### Get result manually

```
bot.set_wait()

bot.execute(1, 2)

if bot.get_result(): print(bot.get_result())

> Waiting for <function <lambda> at 0x10592e3b0> to finish
> Adder is executing task: <function <lambda> at 0x10592e3b0>
> Retrieved result from Adder: 3
> 3
```

## Test

Runs the tests on the BotBoy module

```
make test
```

or

```
python3 test
```
