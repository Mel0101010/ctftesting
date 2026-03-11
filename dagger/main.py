import dagger
import anyio
import argparse
import os
import re


def parse_port_from_dockerfile(dockerfile_path: str) -> int:
    """Parse the first EXPOSE port from a Dockerfile."""
    with open(dockerfile_path) as f:
        for line in f:
            m = re.match(r"^EXPOSE\s+(\d+)", line.strip())
            if m:
                return int(m.group(1))
    raise ValueError(f"No EXPOSE directive found in {dockerfile_path}")


def discover_challenges(ctf_path: str) -> list[dict]:
    """Walk ctf_path and find all challenge directories.

    A challenge directory must contain:
      - Dockerfile
      - solve.py
      - flag.txt
    """
    challenges = []
    for root, dirs, files in os.walk(ctf_path):
        dirs.sort()
        if {"Dockerfile", "solve.py", "flag.txt"}.issubset(files):
            rel = os.path.relpath(root, ctf_path)
            parts = rel.split(os.sep)
            category = parts[0] if len(parts) > 1 else "misc"
            name = parts[-1]
            challenges.append(
                {
                    "label": f"[{category.upper():<6}] {name}",
                    "category": category,
                    "name": name,
                    "path": root,
                    "port": parse_port_from_dockerfile(
                        os.path.join(root, "Dockerfile")
                    ),
                }
            )
    return challenges


async def run_challenge(client: dagger.Client, challenge: dict) -> bool:
    """Build the challenge service, run solve.py, compare output with flag.txt."""
    label = challenge["label"]
    path = challenge["path"]
    port = challenge["port"]

    # Expected flag
    with open(os.path.join(path, "flag.txt")) as f:
        expected_flag = f.read().strip()

    challenge_dir = client.host().directory(path)

    # Challenge runs as a Dagger service
    service = (
        challenge_dir.docker_build()
        .with_exposed_port(port)
        .as_service()
    )

    # Solver container — shares the same challenge directory
    solver = (
        client.container()
        .from_("python:3.11-slim")
        .with_directory("/solve", challenge_dir)
        .with_workdir("/solve")
    )

    # Install solve dependencies if requirements.txt is present
    if os.path.exists(os.path.join(path, "requirements.txt")):
        solver = solver.with_exec(
            ["pip", "install", "-r", "requirements.txt", "-q"]
        )

    solver = solver.with_service_binding("challenge", service).with_exec(
        ["python", "solve.py"]
    )

    try:
        output = await solver.stdout()
        found_flag = output.strip()
        if found_flag == expected_flag:
            print(f"  ✅  {label}  →  {found_flag}")
            return True
        else:
            print(f"  ❌  {label}")
            print(f"       expected : {expected_flag}")
            print(f"       got      : {found_flag}")
            return False
    except Exception:
        stderr = await solver.stderr()
        print(f"  💥  {label}  →  CRASH")
        print(f"       {stderr.strip()}")
        return False


async def main() -> None:
    parser = argparse.ArgumentParser(
        description="Automatically build, solve and validate CTF challenges with Dagger."
    )
    parser.add_argument(
        "ctf_path",
        nargs="?",
        default="./challenges",
        help="Path to the CTF folder (default: ./challenges)",
    )
    args = parser.parse_args()

    ctf_path = os.path.abspath(args.ctf_path)
    if not os.path.isdir(ctf_path):
        print(f"Error: '{ctf_path}' is not a directory.")
        return

    challenges = discover_challenges(ctf_path)
    if not challenges:
        print(
            f"No challenges found in '{ctf_path}'.\n"
            "Each challenge directory must contain: Dockerfile, solve.py, flag.txt"
        )
        return

    print(f"\n=== CTF Challenge Testing ===")
    print(f"  Path  : {ctf_path}")
    print(f"  Found : {len(challenges)} challenge(s)\n")

    results = []
    async with dagger.Connection() as client:
        for challenge in challenges:
            ok = await run_challenge(client, challenge)
            results.append(ok)

    passed = sum(results)
    total = len(results)
    print(f"\n  {passed}/{total} challenge(s) passed.\n")


anyio.run(main)
