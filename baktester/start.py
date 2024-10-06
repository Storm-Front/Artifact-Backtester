import click
import subprocess
import colorama

colorama.init()


@click.command()
@click.option('--build-container', default=False, help="Build the main container")
def build_container(build_container, ):
    command_container=["docker","compose","up"]
    # command_requirements=["pip3","freeze"]

    if build_container:
        # requirements=subprocess.check_output(command_requirements, text=True)

        # with open("server/requirements.txt","w")as f:
        #     f.write(requirements)
        subprocess.run(command_container+["--build"])

    else:
        subprocess.run(["docker","compose","up"] )

if __name__=='__main__':
    build_container()