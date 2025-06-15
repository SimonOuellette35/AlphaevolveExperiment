import asyncio
from openevolve import OpenEvolve

async def main():
    # Initialize the system
    evolve = OpenEvolve(
        initial_program_path="ARC-AGI/initial_program.py",
        evaluation_file="ARC-AGI/evaluator.py",
        config_path="ARC-AGI/config.yaml"
    )

    # Run the evolution
    best_program = await evolve.run(iterations=1000)
    print(f"Best program metrics:")
    for name, value in best_program.metrics.items():
        print(f"  {name}: {value:.4f}")

if __name__ == "__main__":
    asyncio.run(main())