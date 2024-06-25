import click
from kubernetes import config
from HPA import HPA

def validate_scale(value):
    if value not in ['max', 'min']:
        raise click.BadParameter(f'Invalid scale: {value}. Choose from "max" or "min".')
    return value

@click.group()
def cli():
    pass

@cli.command()
@click.argument('scale', type=validate_scale)
@click.option('-n', default="default", help='Nombre de namespaces')
@click.option('-i', is_flag=True, help='Modo iteractivo')
@click.option('-f', default="./hpas.yaml", help='Path archivo config')
def hpa(n, f, scale, i=False):
    obj = HPA(n)
    if i:
        if scale == "max":
            obj.max_replica_iteractivo()
        elif scale == "min":
            obj.min_replica_iteractivo()
    else:
        if scale == "max":
            obj.max_replica_file(f)
        elif scale == "min":
            obj.min_replica_file(f)

@cli.command()
@click.option('-n', default="default", help='Nombre de namespaces')
@click.option('-f', default="./hpas.yaml", help='Path archivo config')
def getfilehpa(n, f):
    obj = HPA(n)
    obj.createFileHpa(f)

if __name__ == '__main__':
    config.load_kube_config()
    cli()