// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
pragma experimental ABIEncoderV2;

import "./SafeMath.sol";

contract ProductFactory {
    event NewProduct(uint256 id, string name);

    event AddAction(uint256 id, string action);

    using SafeMath for uint256;
    using SafeMath16 for uint16;
    using SafeMath32 for uint32;

    struct Product {
        string name;
        uint256[] times;
        string[] actions;
    }

    // Product list of a farmer
    Product[] public products;

    mapping(uint256 => address) public productToOwner;
    mapping(address => uint256) ownerProductCount;

    function createProduct(string memory _name) public{
        uint256[] memory times;
        string[] memory actions;
        products.push(Product(_name, times, actions));
        uint256 id = products.length - 1;
        productToOwner[id] = msg.sender;
        ownerProductCount[msg.sender] = ownerProductCount[msg.sender].add(1);
        emit NewProduct(id, _name);
    }

    modifier onlyOwnerOf(uint256 _id) {
        require(msg.sender == productToOwner[_id]);
        _;
    }

    function addActionToProduct(string memory _action, uint256 _id)
        public
        onlyOwnerOf(_id)
    {
        require(_id < products.length);
        products[_id].times.push(uint256(block.timestamp));
        products[_id].actions.push(_action);
        emit AddAction(_id, _action);
    }

    function getActionFromProduct(uint256 _id)
        public
        view
        returns (uint256[] memory, string[] memory)
    {
        require(_id < products.length);
        Product memory p = products[_id];

        string[] memory actions = p.actions;
        uint256[] memory times = p.times;
        return (times, actions);
    }
}
