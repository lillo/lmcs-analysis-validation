pragma solidity >=0.4.22 <0.6.0;

contract Lottery {
    address public owner;
    address payable player0;
    address payable player1;
    address payable winner;
    bytes32 hash0;
    bytes32 hash1;
    string secret0;
    string secret1;

    // W = owner, state
    constructor() public {
        owner = msg.sender;
    }

    // W = player0
    // R = balance
    function join0() payable public {
        require (player0==address(0));
        require (msg.value > .01 ether);
        player0 = msg.sender;
    }

    // W = player1
    // R = balance
    function join1() payable public {
        require (player1==address(0));
        require (msg.value > .01 ether);
        player1 = msg.sender;
    }

    // W = hash0
    // R = player0, hash0
    function commit0(bytes32 h) public {
        require (msg.sender==player0);
        require (hash0==0);
        hash0 = h;
    }

    // W = hash1
    // R = player1, hash1
    function commit1(bytes32 h) public {
        require (msg.sender==player1);
        require (hash1==0);
        hash1 = h;
    }

    // W = secret0
    // R = player0, hash0, hash1
    function reveal0(string memory s) public {
        require (msg.sender==player0);
        require (hash0!=0 && hash1!=0 &&  hash0 != hash1);
        require(keccak256(abi.encodePacked(s))==hash0);
        secret0 = s;
    }

    // W = secret1
    // R = player1, hash0, hash1
    function reveal1(string memory s) public {
        require (msg.sender==player1);
        require (hash0!=0 && hash1!=0 &&  hash0 != hash1);
        require(keccak256(abi.encodePacked(s))==hash1);
        secret1 = s;
    }

    function win() public {
        uint256 l0 = bytes(secret0).length;
        uint256 l1 = bytes(secret1).length;
        require (l0!=0 && l1!=0);
        if ((l0+l1) % 2 == 0) {
            winner = player0;
        }
        else {
            winner = player1;
        }
        winner.transfer(address(this).balance);

        // reset state for next round
        player0 = address(0);
        player1 = address(0);
        hash0 = 0;
        hash1 = 0;
        secret0 = "";
        secret1 = "";
    }

}