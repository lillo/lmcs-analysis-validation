const Lottery = artifacts.require("Lottery")

module.exports = async function (callback){
    try {
      const accounts = await web3.eth.getAccounts()
      const lottery = await Lottery.deployed()
 
      const user1 = accounts[1]
      const user0 = accounts[0]
      const user2 = accounts[2]
      const value0 = "This is a string"
      const hash0 = web3.utils.soliditySha3(value0)
      const value1 = "This is a longer string"
      const hash1 = web3.utils.soliditySha3(value1)

      for(i=0; i < 10; ++i){

        var join0 = await lottery.join0.sendTransaction({from:user1, value: web3.utils.toWei('0.2', 'ether')}) 
        console.log(`User 1 just joined the lottery, called (join0,`, join0.tx, ')')
        var join1 = await lottery.join1.sendTransaction({from:user2, value: web3.utils.toWei('0.2', 'ether')})
        console.log(`User 2 just joined in the lottery, called (join1,`, join1.tx,')')    
        var commit0 = await lottery.commit0.sendTransaction(hash0, {from:user1})
        console.log(`User 1 just committed her value, called (commit0,`, commit0.tx,')')
        var commit1 = await lottery.commit1.sendTransaction(hash1, {from:user2})
        console.log(`User 2 just committed her value, called (commit1,`, commit1.tx,')')    
        var reveal0 = await lottery.reveal0.sendTransaction(value0, {from:user1})
        console.log(`User 1 just revealed her value, called (reveal0,`, reveal0.tx,')')
        var reveal1 = await lottery.reveal1.sendTransaction(value1, {from:user2})
        console.log(`User 2 just revealed her value, called (reveal1,`, reveal1.tx,')')  
        var win = await lottery.win.sendTransaction({from:user0})
        console.log(`User 0 just decided the winner, called (win,`, win.tx,')')
      }
    }catch(error){
        console.log(error)
        callback(error)
        return
    }
    callback()
 }