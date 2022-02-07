# Algorithmic and Human Collusion - oTree experiment

The repository contains all applications to run the experiments used in the paper
["Algorithmic and Human Collusion"](https://tofewe.github.io/Algorithmic_and_Human_Collusion_Tobias_Werner.pdf).


The app uses oTree<5 (Django).

This repository does not contain the simulations or the application to run the experiments. To run the simulations that are described in the paper, please see [here](https://github.com/ToFeWe/qpricesim) and [here](https://github.com/ToFeWe/q-learning-simulation-code).


# Run it locally

1. Create and start local environment.
2. Install the dependencies.
    ```terminal
    pip install -r requirements_base.txt
    ```
3. Run the development server.
    ```terminal
    otree devserver
    ```
4. The application runs at `localhost:8000`.