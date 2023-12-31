import platform
import subprocess


def main():
    system = platform.system()

    if system == "Windows":
        script_path = "scripts\\update_env.bat"
    elif system in ("Linux", "Darwin"):  # Darwin is for macOS
        script_path = "scripts/update_env.sh"
    else:
        print(f"Unsupported system: {system}")
        return

    subprocess.run(script_path, shell=True, check=True)


if __name__ == "__main__":
    main()
