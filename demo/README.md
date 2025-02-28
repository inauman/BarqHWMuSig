# BarqHWMuSig Demo

This directory contains demonstration scripts for the BarqHWMuSig application, which showcases Bitcoin multisignature wallet functionality with hardware device integration.

## Demo Script

The main demo script (`demo.py`) demonstrates the full workflow of the BarqHWMuSig application:

1. **Wallet Creation**: Creates a 2-of-3 multisignature wallet with predefined public keys
2. **Transaction Building**: Creates a transaction that spends from the multisig wallet
3. **Transaction Signing**: Signs the transaction using multiple hardware devices (YubiKey and Ledger)
4. **Transaction Broadcasting**: Simulates broadcasting the signed transaction to the Bitcoin network
5. **Transaction Monitoring**: Simulates monitoring the transaction for confirmations

## Running the Demo

To run the demo, make sure you have set up the BarqHWMuSig environment as described in the main README.

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run the demo script
python demo/demo.py
```

## Notes

- The demo uses mock implementations of hardware devices for demonstration purposes.
- No actual Bitcoin transactions are created or broadcast.
- The demo simulates the full workflow with detailed logging to show what would happen in a real-world scenario.

## Expected Output

The demo will produce detailed logs showing each step of the process, including:

- Environment setup
- Wallet creation with a multisig address
- Transaction creation with inputs and outputs
- Device connection and transaction signing
- Transaction broadcasting (simulated)
- Transaction confirmation monitoring (simulated)

If everything works correctly, you should see a message indicating that the demo completed successfully.

## Troubleshooting

If you encounter any issues running the demo:

1. Make sure all dependencies are installed
2. Check that the virtual environment is activated
3. Verify that the configuration in `.env` is correct
4. Check the logs for specific error messages

For more detailed information about the BarqHWMuSig application, refer to the main README and documentation in the `docs` directory. 