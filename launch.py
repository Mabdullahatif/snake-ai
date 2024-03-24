import subprocess


def main():
    # List of commands to run each script
    commands = [
        ['A*', 'green', 'Maps/hurdlesMaze.txt', 'A*'],
        ['GBFS', 'blue', 'Maps/hurdlesMaze.txt', 'GBFS'],
        ['UCS', 'pink', 'Maps/hurdlesMaze.txt', 'UCS']
    ]

    target = 'main.py'

    # List to store process objects
    processes = []

    # Launch processes for each script
    for command in commands:
        processes.append(subprocess.Popen(['python', target, *command]))

    try:
        # Wait for all processes to complete
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        # Handle Ctrl+C (KeyboardInterrupt) to gracefully terminate processes
        for process in processes:
            process.terminate()


if __name__ == "__main__":
    main()
