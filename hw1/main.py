import argparse
from hw1.utils import PathPlanMode
import hw1.path_finding as pf

def main():
    parser = argparse.ArgumentParser(
        prog="COMSW4701 HW1",
        description="Robot Path Planning",
    )
    parser.add_argument(
        "world_path", help="The the directory containing the world files saved as .npy"
    )
    args = parser.parse_args()

    print("=" * 40)
    print("Testing Grid World Path Planning...")
    print(f"Loading grid world files from path: {args.world_path}")
    print("Modes: 1. DFS, 2. BFS, 3. Gradient ascent, 4. A*")
    pf.test_world(
        1, (20, 0), (95, 60), world_dir=args.world_path, 
        outmode=PathPlanMode.GRAD, inmode=PathPlanMode.DFS
        )
    pf.test_world(
        1, (20, 0), (95, 60), world_dir=args.world_path, 
        outmode=PathPlanMode.GRAD, inmode=PathPlanMode.BFS
    )
    pf.test_world(
        1, (20, 0), (95, 60), world_dir=args.world_path, 
        outmode=PathPlanMode.A_STAR, inmode=PathPlanMode.DFS
        )
    pf.test_world(
        1, (20, 0), (95, 60), world_dir=args.world_path, 
        outmode=PathPlanMode.A_STAR, inmode=PathPlanMode.BFS
    )
    pf.test_world(
        4, (50, 1), (80, 99), world_dir=args.world_path, 
        outmode=PathPlanMode.GRAD, inmode=PathPlanMode.DFS
        )
    pf.test_world(
        4, (50, 1), (80, 99), world_dir=args.world_path, 
        outmode=PathPlanMode.GRAD, inmode=PathPlanMode.BFS
    )
    pf.test_world(
        4, (50, 1), (80, 99), world_dir=args.world_path, 
        outmode=PathPlanMode.A_STAR, inmode=PathPlanMode.DFS
        )
    pf.test_world(
        4, (50, 1), (80, 99), world_dir=args.world_path, 
        outmode=PathPlanMode.A_STAR, inmode=PathPlanMode.BFS
    )
    print("Done")
    print("=" * 40)


if __name__ == "__main__":
    main()
