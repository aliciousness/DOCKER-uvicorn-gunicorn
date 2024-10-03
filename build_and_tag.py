#!/usr/bin/env python3
import argparse
import subprocess

def docker_login():
    '''
    This function handles the Docker login process. It runs the "docker login" command
    and checks the return code to determine if the login was successful. If the login fails,
    it prints a message and retries the login process in a loop until a successful login is achieved.
    This is needed because if you create a new repo on docker hub you will need to login and logout to push the tags initially.
    '''
    login_success = False
    while not login_success:
        result = subprocess.run("docker login", shell=True)
        if result.returncode == 0:
            login_success = True
        else:
            print("Login failed. Please try again.")

def run_docker_commands(version, test, run):
    '''
    To run script, build_and_tag.py <input version of image here>
    After running this script you can check the images in docker desktop and push the tags to dockerhub
    This function sets up the buildx builder instance for multi-architecture builds, builds the Docker images, tags the images and pushes to registry with the specified version.
    '''
    repo = "uvicorn-gunicorn-fastapi"
    base_image_slim = f"aliciousness/{repo}:v{version}-python3.11-bookworm-slim"
    base_image_bookworm = f"aliciousness/{repo}:v{version}-python3.11-bookworm"

    if not test:
        docker_login()

    # Create and use a new buildx builder instance with the docker-container driver
    subprocess.run(f"docker buildx create --use --name {repo} --driver docker-container", shell=True)
    subprocess.run(f"docker buildx inspect {repo} --bootstrap", shell=True)

    build_commands = [
        f"docker buildx build --build-arg IMAGE_VERSION={version} --platform linux/amd64 -t {base_image_slim}-amd64 -f 3.11/bookworm-slim/Dockerfile --load .",
        f"docker buildx build --build-arg IMAGE_VERSION={version} --platform linux/arm64 -t {base_image_slim}-arm64 -f 3.11/bookworm-slim/Dockerfile --load .",
        f"docker buildx build --build-arg IMAGE_VERSION={version} --platform linux/amd64 -t {base_image_bookworm}-amd64 -f 3.11/bookworm/Dockerfile --load .",
        f"docker buildx build --build-arg IMAGE_VERSION={version} --platform linux/arm64 -t {base_image_bookworm}-arm64 -f 3.11/bookworm/Dockerfile --load ."
    ]
    if not test:
        for command in build_commands:
            subprocess.run(command, shell=True)
    else:
        subprocess.run(build_commands[1], shell=True)
    
    if not test:
        tag_commands = [
            f"docker buildx imagetools create --tag aliciousness/{repo}:latest {base_image_slim}-amd64 {base_image_slim}-arm64",
            f"docker buildx imagetools create --tag aliciousness/{repo}:python3 {base_image_slim}-amd64 {base_image_slim}-arm64",
            f"docker buildx imagetools create --tag aliciousness/{repo}:python3.11 {base_image_slim}-amd64 {base_image_slim}-arm64",
            f"docker buildx imagetools create --tag aliciousness/{repo}:v{version}-python3-slim {base_image_slim}-amd64 {base_image_slim}-arm64",
            f"docker buildx imagetools create --tag aliciousness/{repo}:v{version}-python3-debian {base_image_slim}-amd64 {base_image_slim}-arm64",
            f"docker buildx imagetools create --tag aliciousness/{repo}:v{version}-python3-bookworm {base_image_bookworm}-amd64 {base_image_bookworm}-arm64",
            f"docker buildx imagetools create --tag aliciousness/{repo}:v{version}-bookworm {base_image_bookworm}-amd64 {base_image_bookworm}-arm64"
        ]

        for command in tag_commands:
            subprocess.run(command, shell=True)
    
    # Remove the buildx container after successful build
    subprocess.run(f"docker buildx rm {repo}", shell=True)

    if run:
        run_command = f"docker run -d --name {repo}_container {base_image_slim}-amd64"
        subprocess.run(run_command, shell=True)
        print(f"Running command: {run_command}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build and tag Docker images.')
    parser.add_argument('version', type=str, help='The version to use for tagging the Docker images.')
    parser.add_argument('--test', action='store_true', help='Build images without pushing to any registry.')
    parser.add_argument('--run', action='store_true', help='Run a command for the first build only.')

    args = parser.parse_args()

    run_docker_commands(args.version, args.test, args.run)
