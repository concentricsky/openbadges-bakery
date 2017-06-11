import click

from . import utils


@click.group()
def cli():
    pass


@click.command()
@click.argument('input_file', type=click.File('rb'))
@click.argument('output_file', type=click.File('wb'))
@click.option('--data', type=str, prompt=True)
def bake(input_file, output_file, data):
	"""
	This command bakes Open Badges data into a file and saves
	the result to an output file.
	
	Positional Arguments:

	\b
	  Input filename:    File must exist.
	\b
	  Output filename:   If file exists, it will be overwritten.
	"""
	output = utils.bake(input_file, data, output_file)

	click.echo(
		"{} is done baking. Remember to let it cool".format(output_file.name)
	)


@click.command()
@click.argument('input_file', type=click.File('rb'))
@click.argument('output_file', type=click.File('wb'), default='-')
def unbake(input_file, output_file):
	"""
	This command extracts Open Badges data from an image and
	prints it to a file or the standard output.

	Positional Arguments:

	\b
	  Input filename:    File must exist.
	\b
	  Output filename:   If file exists, it will be overwritten.
	"""
	click.echo('')
	output_file.write(utils.unbake(input_file))
	click.echo('\n')


cli.add_command(bake)
cli.add_command(unbake)

if __name__ == '__main__':
    cli()
