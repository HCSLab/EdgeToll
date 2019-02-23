var Migrations = artifacts.require('./Migrations.sol');
// var PC = artifacts.require('./PC.sol');

module.exports = function (deployer) {
  deployer.deploy(Migrations);
  // deployer.deploy(PC);
}
