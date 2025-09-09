#!/bin/bash
python3 simulators/simulator.py --id moto_1 --interval 2 &
python3 simulators/simulator.py --id moto_2 --interval 2.5 &
python3 simulators/simulator.py --id moto_3 --interval 3 &
echo "Simuladores iniciados (moto_1, moto_2, moto_3)."
