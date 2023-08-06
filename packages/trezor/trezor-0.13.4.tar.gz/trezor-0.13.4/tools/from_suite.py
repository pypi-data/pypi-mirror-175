#!/usr/bin/env python3
import decimal
import json
from typing import Any

import click
import requests

from trezorlib import btc
from trezorlib.protobuf import to_dict

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "trezorlib"})


def echo(*args: Any, **kwargs: Any) -> Any:
    return click.echo(*args, err=True, **kwargs)


def prompt(*args: Any, **kwargs: Any) -> Any:
    return click.prompt(*args, err=True, **kwargs)


def read_snippet(prompt: str) -> Any:
    echo(prompt)
    json_in = ""
    while True:
        json_in += input()
        try:
            return json.loads(json_in)
        except Exception:
            pass


@click.command()
@click.option("-b", "--blockbook", default="btc1.trezor.io", help="Blockbook API host")
@click.option("-c", "--coin", default="Bitcoin", help="Coin to use")
@click.option("-v", "--version", type=int, default=2, help="Transaction version")
def cli(blockbook: str, coin: str, version: int) -> None:
    """
    Build a tx json compatible with `trezorctl btc sign-tx`, from a Suite debug output.
    """
    if not SESSION.get(f"https://{blockbook}/api/block/1").ok:
        raise click.ClickException("Could not connect to blockbook")

    blockbook_url = f"https://{blockbook}/api/tx-specific/"

    inputs_json = read_snippet("Please input the transaction inputs JSON block.")

    prev_txes = {}

    for inp in inputs_json:
        prev_tx = prev_txes.get(inp["prev_hash"])
        if not prev_tx:
            prev_tx = SESSION.get(blockbook_url + inp["prev_hash"]).json(parse_float=decimal.Decimal)
            prev_txes[inp["prev_hash"]] = to_dict(btc.from_json(prev_tx))

    outputs_json = read_snippet("Please input the transaction outputs JSON block.")

    result = dict(
        coin_name=coin,
        inputs=inputs_json,
        outputs=outputs_json,
        prev_txes=prev_txes,
        details=dict(version=version),
    )
    print(json.dumps(result, indent=2))
    print()


if __name__ == "__main__":
    cli()
