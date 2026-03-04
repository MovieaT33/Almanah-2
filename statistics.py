import sys

import matplotlib.pyplot as plt


def main() -> None:
    # Check command-line arguments
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <filename>")
        sys.exit(1)

    filename: str = sys.argv[1]

    # Read data from the file
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines: list[str] = f.readlines()
    except OSError as exc:
        print(f"\03[31merror\033[0m: {exc}")
        sys.exit(1)

    # Convert lines to floats
    try:
        data: list[float] = [float(line.strip())
                             for line in lines if line.strip()]
    except ValueError as exc:
        print(f"\033[31merror\033[0m: converting data to float: {exc}")
        sys.exit(2)

    if not data:
        print("\033[31merror\033[0m: no data found in the file")
        sys.exit(3)

    # Plot the data
    plt.figure(figsize=(8, 5))
    plt.plot(data, marker="o", linestyle="-", color="blue")
    plt.title("Data Plot from File")
    plt.xlabel("Data Point Index")
    plt.ylabel("Value")
    plt.grid(True)

    # Save the plot
    output_file: str = f"{filename}.png"
    plt.savefig(output_file)
    print(f"Plot saved as '{output_file}'")

    plt.show()

if __name__ == "__main__":
    main()
