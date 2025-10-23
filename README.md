# Jute Patti Simulation

A simulation of the card game **Jute Patti**, to test if any player holds an advantage in a 1v1 game.

## 1v1 Dealer Disadvantage

My brother said that the player who deals has a disadvantage in a regular 1v1, so I made a simulation to check.  
After simulating **5 million games**, the results show:

> The dealer (Player 2) has around a **3.4% disadvantage**.

![Simulation Results](https://github.com/user-attachments/assets/83b950d3-1dd2-4ad7-bdd4-b11a92968921)

I’m not sure why this happens yet, but it’s consistent across large samples.

## How to Run

No external dependencies required.

### Simulate one game
```bash
python main.py
````

### Simulate 5000 games (default)

```bash
python main.py --simulate
```

### Simulate n games (custom)

```bash
python main.py --simulate n
```

Replace `n` with any integer.

