"""
Main entry point for the BarqHWMuSig application.

This module provides the main entry point for the BarqHWMuSig application,
which is a proof-of-concept implementation of a 2-of-3 Bitcoin multisig wallet
with hardware device integration.
"""

from src.cli.wallet_cli import cli


if __name__ == "__main__":
    cli(obj={}) 