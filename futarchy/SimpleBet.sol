// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * SimpleBet - A minimal prediction market for testing
 *
 * Question: "Will $NOICE price be higher than [startPrice] on [endTime]?"
 *
 * How it works:
 * 1. Creator deploys with a question and end time
 * 2. Users bet ETH on YES or NO
 * 3. After endTime, resolver calls resolve(true/false)
 * 4. Winners claim proportional share of the pool
 */
contract SimpleBet {
    address public resolver;
    string public question;
    uint256 public endTime;
    uint256 public startPrice; // in wei, for reference

    bool public resolved;
    bool public outcome; // true = YES won, false = NO won

    uint256 public totalYes;
    uint256 public totalNo;

    mapping(address => uint256) public yesBets;
    mapping(address => uint256) public noBets;
    mapping(address => bool) public claimed;

    event BetPlaced(address indexed user, bool isYes, uint256 amount);
    event MarketResolved(bool outcome);
    event Claimed(address indexed user, uint256 amount);

    constructor(
        string memory _question,
        uint256 _durationSeconds,
        uint256 _startPrice
    ) {
        resolver = msg.sender;
        question = _question;
        endTime = block.timestamp + _durationSeconds;
        startPrice = _startPrice;
    }

    function betYes() external payable {
        require(block.timestamp < endTime, "Market closed");
        require(msg.value > 0, "Must send ETH");
        require(!resolved, "Already resolved");

        yesBets[msg.sender] += msg.value;
        totalYes += msg.value;

        emit BetPlaced(msg.sender, true, msg.value);
    }

    function betNo() external payable {
        require(block.timestamp < endTime, "Market closed");
        require(msg.value > 0, "Must send ETH");
        require(!resolved, "Already resolved");

        noBets[msg.sender] += msg.value;
        totalNo += msg.value;

        emit BetPlaced(msg.sender, false, msg.value);
    }

    function resolve(bool _outcome) external {
        require(msg.sender == resolver, "Only resolver");
        require(block.timestamp >= endTime, "Too early");
        require(!resolved, "Already resolved");

        resolved = true;
        outcome = _outcome;

        emit MarketResolved(_outcome);
    }

    function claim() external {
        require(resolved, "Not resolved yet");
        require(!claimed[msg.sender], "Already claimed");

        uint256 payout = 0;
        uint256 totalPool = totalYes + totalNo;

        if (outcome) {
            // YES won
            if (yesBets[msg.sender] > 0 && totalYes > 0) {
                payout = (yesBets[msg.sender] * totalPool) / totalYes;
            }
        } else {
            // NO won
            if (noBets[msg.sender] > 0 && totalNo > 0) {
                payout = (noBets[msg.sender] * totalPool) / totalNo;
            }
        }

        require(payout > 0, "Nothing to claim");
        claimed[msg.sender] = true;

        (bool success, ) = msg.sender.call{value: payout}("");
        require(success, "Transfer failed");

        emit Claimed(msg.sender, payout);
    }

    // View functions
    function getPoolState() external view returns (
        uint256 _totalYes,
        uint256 _totalNo,
        uint256 _endTime,
        bool _resolved,
        bool _outcome
    ) {
        return (totalYes, totalNo, endTime, resolved, outcome);
    }

    function getUserBets(address user) external view returns (
        uint256 _yesBet,
        uint256 _noBet,
        bool _claimed
    ) {
        return (yesBets[user], noBets[user], claimed[user]);
    }

    function getImpliedProbability() external view returns (
        uint256 yesPct,
        uint256 noPct
    ) {
        uint256 total = totalYes + totalNo;
        if (total == 0) return (50, 50);
        yesPct = (totalYes * 100) / total;
        noPct = (totalNo * 100) / total;
    }
}
