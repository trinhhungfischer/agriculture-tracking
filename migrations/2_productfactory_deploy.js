const ProductFactory = artifacts.require("ProductFactory");

module.exports = function (deployer) {
  deployer.deploy(ProductFactory);
};
