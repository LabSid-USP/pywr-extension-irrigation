# Pywr Extended Node for Irrigation Water Demand

This repository contains a Pywr extended node that adds functionality to manage irrigation demands based on soil water balance. The software is designed to estimate the water demands according to the soil's water content and crop type. This tool has been developed as part of a research project. The Pywr with irrigation extended node allows to use all the nodes from original source, including Hydropowers, ground water and hydroeconomic.

## Features

- **Irrigation Water Demand**: A extended node that estimate water demands based on soil water balance method.
- **Integrated with Pywr**: Leverages the Pywr framework for water resource modeling and optimization.
- **Supports Multiple Scenarios**: The package includes usage examples demonstrating different scenarios of irrigation water demand in the Upper Batalha river (Brazil).

## Installation

This package uses [Miniforge/Conda](https://github.com/conda-forge/miniforge) for dependency management. To install the package and its dependencies, follow the steps below:

1. Clone the repository:

   ```bash
   git clone https://github.com/LabSid-USP/pywr-extension-irrigation.git
   cd pywr-irrigation-node
   ```

2. Install Miniforge if you don't already have it. You can follow the instructions [here](https://github.com/conda-forge/miniforge);

3. Create a Conda environment and install the required dependencies:

   ```bash
    conda create --name pywr_irrigation -c conda-forge python=3.12 pywr
    conda activate pywr_irrigation
   ```

## Usage

The custom Pywr node can be used in water resource simulations to manage irrigation demand based on soil water balance. Below are some examples located in the `examples/` directory to help you get started.

### Running the Examples

There are four example scenarios included:

1. Example based on economic aspects with irrigation extented node: examples\hydroecon_with_irrigation_node\run_allocation_hydroecon_with_irr.py;
2. Example based on economic aspects without irrigation extended node: examples\hydroecon_without_irrigation_node\run_allocation_hydroecon_without_irr.py;
3. Example Prority based with irrigation extended node: examples\with_irrigation_node\run_allocation_with_irr.py;
4. Example Priority based without irrigation extended node: examples\without_irrigation_node\run_allocation_without_irr.py.

You can run these examples as follows:

```bash
cd examples
python ./with_irrigation_node/run_allocation_with_irr.py
```

Replace `./with_irrigation_node/run_allocation_with_irr.py` with any of the other examples (`./hydroecon_without_irrigation_node/run_allocation_hydroecon_without_irr.py`, `./with_irrigation_node/run_allocation_with_irr.py`, or `./without_irrigation_node/run_allocation_without_irr.py`) to explore different scenarios.

You can find the results in ./results folder. All discharges in Pywr are in volume/day (m³/day)

## Contributing

We welcome contributions from the community. If you find a bug or have a feature request, please open an issue or submit a pull request.

## License

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.

## Citation

If you use this software in your research, please cite the corresponding article (once published) or refer to the preprint available [here](https://github.com/LabSid-USP/pywr-extension-irrigation).

---

For any inquiries, feel free to reach out to the development team via the repository's issue tracker.
