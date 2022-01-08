// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
pragma experimental ABIEncoderV2;

import "./ProductFactory.sol";

contract ProductHelper is ProductFactory {
    function getProductsByOwner(address _owner) external view returns(uint[] memory, string[] memory) {
        uint[] memory result = new uint[](ownerProductCount[_owner]);
        string[] memory names = new string[](ownerProductCount[_owner]);
        uint counter = 0;
        for (uint i = 0; i < products.length; i++) {
            if (productToOwner[i] == _owner) {
                result[counter] = i;
                names[counter] = products[i].name; 
                counter++;
            }
        }
        return (result, names);
    }
}