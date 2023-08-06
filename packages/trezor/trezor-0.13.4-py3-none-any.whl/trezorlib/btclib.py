# This file is part of the Trezor project.
#
# Copyright (C) 2012-2022 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

from btclib.tx.tx import Tx  # noqa: I900
from btclib.tx.tx_in import TxIn  # noqa: I900
from btclib.tx.tx_out import TxOut  # noqa: I900

from . import messages


def to_input(txin: TxIn) -> messages.TxInputType:
    return messages.TxInputType(
        prev_hash=txin.prev_out.tx_id,
        prev_index=txin.prev_out.vout,
        script_sig=txin.script_sig,
        sequence=txin.sequence,
    )


def to_bin_output(txout: TxOut) -> messages.TxOutputBinType:
    return messages.TxOutputBinType(
        amount=txout.value,
        script_pubkey=txout.script_pub_key.script,
    )


def to_prevtx(tx: Tx) -> messages.TransactionType:
    inputs = [to_input(txin) for txin in tx.vin]
    outputs = [to_bin_output(txout) for txout in tx.vout]
    return messages.TransactionType(
        version=tx.version,
        inputs=inputs,
        bin_outputs=outputs,
        lock_time=tx.lock_time,
    )
