const Sequelize = require("sequelize")
const sequelize = require("../util/db.js")

const Track_Record = sequelize.define("TrackRecord", {
    DATE: {
        type: Sequelize.TEXT,
        allowNull: false,
    },
    Location: {
        type: Sequelize.STRING,
        allowNull: false,
    },
    Description: {
        type: Sequelize.TEXT,
        allowNull: false,
    },
    Status: {
        type: Sequelize.TEXT,
        allowNull: false,
    },
    PtwNo: {
        type: Sequelize.BIGINT,
        allowNull: false,
    },
    Image: {
        type: Sequelize.STRING,
        allowNull: true,
    },
    ManHours: {
        type: Sequelize.INTEGER,
        allowNull: false,
    },
    


})
module.exports = Track_Record