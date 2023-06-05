const config = require("../config.json")
const Sequelize = require("sequelize")

const sequelize = new Sequelize(config.dbUrl)

sequelize
    .authenticate()
    .then(() => {
        console.log("Connection has been established successfully.")
    })
    .catch((err) => {
        console.error("Unable to connect to the database:", err)
    })

module.exports = sequelize