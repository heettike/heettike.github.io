# futarchy betting - deployment guide

## what you need

1. **MetaMask** wallet with some ETH on Base (you need ~$5-10 worth for deployment + gas)
2. **Chrome browser** (or any browser with MetaMask)

that's it. no accounts, no CLI, no coding required.

---

## step 1: get ETH on Base

if you don't have ETH on Base:
- go to [bridge.base.org](https://bridge.base.org)
- bridge ETH from Ethereum mainnet to Base
- or buy ETH directly on Coinbase and withdraw to Base

---

## step 2: open Remix IDE

1. go to [remix.ethereum.org](https://remix.ethereum.org)
2. this is a browser-based Solidity IDE - no installation needed

---

## step 3: create the contract file

1. in Remix, look at the left sidebar under "File Explorer"
2. click the "+" icon to create a new file
3. name it `SimpleBet.sol`
4. copy-paste the entire contents of `SimpleBet.sol` from this folder into Remix

---

## step 4: compile the contract

1. in the left sidebar, click the **Solidity Compiler** tab (icon looks like "S")
2. make sure compiler version is `0.8.19` or higher
3. click **Compile SimpleBet.sol**
4. you should see a green checkmark when done

---

## step 5: deploy the contract

1. in the left sidebar, click the **Deploy & Run** tab (icon looks like →)
2. under "ENVIRONMENT", select **Injected Provider - MetaMask**
3. MetaMask will popup - connect your wallet
4. make sure you're on **Base** network (chain ID 8453)

5. under "CONTRACT", select **SimpleBet**

6. expand the "Deploy" section - you need to fill in 3 parameters:
   - `_question`: `"will $noice price be higher than today's price in 7 days?"`
   - `_durationSeconds`: `604800` (this is 7 days in seconds)
   - `_startPrice`: `0` (or current price in wei - doesn't affect betting)

7. click **transact**
8. MetaMask will popup - confirm the transaction
9. wait for confirmation (usually 1-5 seconds on Base)

---

## step 6: copy your contract address

1. after deployment, look at the bottom of the "Deploy & Run" panel
2. under "Deployed Contracts", you'll see your contract
3. click the copy icon next to the contract address
4. it looks like: `0x1234...abcd`

**SAVE THIS ADDRESS** - you need it for the frontend

---

## step 7: update the frontend

1. open `index.html` in a text editor
2. find this line (around line 459):
   ```javascript
   const CONTRACT_ADDRESS = "0x0000000000000000000000000000000000000000";
   ```
3. replace the zero address with your deployed contract address:
   ```javascript
   const CONTRACT_ADDRESS = "0xYOUR_CONTRACT_ADDRESS_HERE";
   ```
4. save the file

---

## step 8: test it

1. open `index.html` in your browser (or push to GitHub Pages)
2. click "connect wallet"
3. you should see the market with your question
4. try betting 0.001 ETH on YES or NO
5. check that the pool updates

---

## how it works

- anyone can bet YES or NO by sending ETH
- after 7 days (`_durationSeconds`), betting closes
- the resolver (you, the deployer) calls `resolve(true)` or `resolve(false)`
- winners split the entire pool proportionally

---

## resolving the market

after the deadline, you (as resolver) need to settle the market:

1. go back to Remix
2. find your deployed contract under "Deployed Contracts"
3. expand it and find the `resolve` function
4. enter `true` if YES won (price went up) or `false` if NO won
5. click "transact" and confirm in MetaMask

---

## costs

- **deployment**: ~0.001-0.002 ETH ($3-5)
- **betting**: ~0.0001 ETH per bet ($0.30)
- **resolving**: ~0.0001 ETH ($0.30)

Base is cheap. your $10 test will work fine.

---

## troubleshooting

**"contract not deployed yet" shows in UI**
- you haven't updated CONTRACT_ADDRESS in index.html yet

**MetaMask won't connect**
- make sure you're on Base network
- try refreshing the page

**transaction fails**
- check you have enough ETH for gas
- make sure market hasn't ended yet (for betting)

---

## questions?

this is an MVP. it works, but it's basic. the contract:
- has no fees
- requires manual resolution
- uses ETH directly (not tokens)

for a production version, you'd want:
- oracle integration for automatic resolution
- ERC-20 token support
- fee mechanism
