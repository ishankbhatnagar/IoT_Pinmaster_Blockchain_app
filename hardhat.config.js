//21BCT0097 ISHANK BHATNAGAR
// Exporting the module to be used by Hardhat
module.exports = {
  // Specifying the Solidity compiler version to be used in the project
  solidity: "0.8.21",

  // Configuration for different networks
  networks: {
    // Configuration specific to the Hardhat network
    hardhat: {
      // The chain ID for the Hardhat network. The default value for Hardhat is 1337.
      // This chain ID is used to distinguish between different blockchain networks.
      chainId: 1337, // Default chainId for Hardhat network
    }
  }
};
