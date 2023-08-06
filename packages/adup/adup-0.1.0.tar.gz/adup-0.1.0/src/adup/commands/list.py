# Copyright Olivier ORABONA <olivier.orabona@gmail.com> and contributors.
# All Rights Reserved.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import sys

import click
from tabulate import tabulate

from adup.cli import cli
from adup.logging import debug, error, info, warn
from adup.utils import get_engine, get_matching_conditions, get_multi_value_option


@click.group()
def cli():  # noqa: F811
    pass


@cli.command()
@click.option(
    "-t",
    "--type",
    "conditions",
    type=click.Choice(["samehash4k", "samehash", "samemtime", "samesize", "samename", "all", "every"]),
    default="samehash",
)
@click.argument(
    "operation",
    nargs=1,
    type=click.Choice(["selected", "unselected", "all"]),
    default="all",
)
@click.option(
    "--hide",
    "hideColumns",
    default=[],
    help="Hide columns.",
    type=click.Choice(["name", "path", "size", "mtime", "hash", "hash4k"]),
    multiple=True,
)
@click.option(
    "--show",
    "showColumns",
    default=[],
    help="Show columns.",
    type=click.Choice(["name", "path", "size", "mtime", "hash", "hash4k"]),
    multiple=True,
)
@click.pass_obj
def cli(ctx, conditions, operation, hideColumns, showColumns):
    """
    List files as they are detected in the duplicates database.
    """
    # Get backend from config file
    get_engine(ctx.config)

    # Process conditions
    debug("Conditions given in command line: {}".format(conditions))
    listOfConditions = get_matching_conditions([conditions])
    debug("List of conditions to apply:")
    for condition in listOfConditions:
        debug(" - {}".format(" and ".join(condition)))

    # Show columns takes precedence over hide columns
    # and command line takes precedence over config file
    _hide_columns = list(hideColumns) + get_multi_value_option(ctx.config["command.list"], "hide_columns[]", [])
    _show_columns = list(showColumns) + get_multi_value_option(ctx.config["command.list"], "show_columns[]", [])
    debug("Hide columns: {}".format(_hide_columns))
    debug("Show columns: {}".format(_show_columns))
    columns_to_hide = set(_hide_columns) - set(_show_columns)

    debug("Definitive list of columns to hide:")
    for column in columns_to_hide:
        debug(" - {}".format(column))

    info(f"Listing files marked as {operation} for condition '{conditions}'.")

    # Let the backend do the job
    try:
        from adup.backends import list_duplicates

        columns, results = list_duplicates(operation, listOfConditions, columns_to_hide)
    except Exception as exc:  # pragma: no cover
        error("FATAL: cannot execute command in database: %s" % exc)
        sys.exit(1)

    # tabulate results
    if len(results) > 0:
        click.secho(tabulate(results, headers=[name for name in columns], tablefmt="psql"))
        index = [index for index, name in enumerate(columns) if name == "size"][0]
        totalSize = sum(x[index] for x in results)
        click.secho(f"Total: {len(results)} files / {totalSize} bytes", bold=True)
    else:
        warn(f"No {operation} duplicates found for this combination '{conditions}' !")

    sys.exit(0)
