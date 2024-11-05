# Examples
The Pywr irrigation extended node can be used in water resource optimization to manage irrigation demand based on soil water balance. Below are some examples located in the `examples/` directory to help you get started.

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
