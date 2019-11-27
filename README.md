# PSO Labyrinth

## Usage

### Options:
 - `-i` Input file path
 - `-o` Output file path
 - `-s` Seed for np.random
 - `-c` Config file path (default: `config.json`)

### Configuration:
The script needs config file to run in json format. Values:

| variable | description |
| --- | --- |
|`c1`| Coefficient used in PSO algorythm - weight of the last velocity of a particle |
|`c2`| Coefficient used in PSO algorythm - weight of the best solution achieved by a particle |
|`c3`| Coefficient used in PSO algorythm - weight of the best solution achieved by all particles |
|`size`| Size of the square board |
|`paths`| # of particles (path-looking instances) |
|`maxlen`| Maximum length of the path |
|`iters`| Iterations, in which particles will try to find the best solution |
|`coin_density`| Chance for a coin to appear on a random field |

### Examples:
Run:

```
python3 pso.py -s 19686901 -o board.npy
```

Config file:

```
{
    "c1": 1.0,
    "c2": 0.8,
    "c3": 1.0,
    "size": 15,
    "paths": 5,
    "maxlen": 7,
    "iters": 400,
    "coin_density": 0.4
}
```
