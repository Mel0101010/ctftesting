import dagger
import anyio

async def run_challenge(client, name, challenge_dir, port, solve_script, pip_deps=None):
    """Build challenge, start it as a service, run the solve script."""
    service = (
        client.host().directory(challenge_dir)
        .docker_build()
        .with_exposed_port(port)
        .as_service()
    )

    base = (
        client.container()
        .from_("python:3.11")
        .with_directory("/solve", client.host().directory("./solve"))
        .with_workdir("/solve")
    )

    if pip_deps:
        base = base.with_exec(["pip", "install"] + pip_deps)

    solver = (
        base
        .with_service_binding("challenge", service)
        .with_exec(["python", solve_script])
    )

    exit_code = await solver.exit_code()
    if exit_code == 0:
        print(f"  {name} validated")
    else:
        output = await solver.stderr()
        print(f"  {name} failed\n{output}")

async def main():
    async with dagger.Connection() as client:
        print("\n=== CTF Challenge Testing ===\n")

        await run_challenge(
            client,
            name="[WEB]    chall1 - Flask admin bypass",
            challenge_dir="./challenges/web/chall1",
            port=5000,
            solve_script="solve.py",
            pip_deps=["requests"],
        )

        await run_challenge(
            client,
            name="[CRYPTO] chall1 - XOR cipher",
            challenge_dir="./challenges/crypto/chall1",
            port=5001,
            solve_script="crypto_solve.py",
        )

        await run_challenge(
            client,
            name="[PWN]    chall1 - Buffer overflow",
            challenge_dir="./challenges/pwn/chall1",
            port=5002,
            solve_script="pwn_solve.py",
        )

        print()

anyio.run(main)
