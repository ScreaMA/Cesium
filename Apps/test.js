var mysql      = require('mysql');
var connection = mysql.createConnection({
    host     : '104.238.141.111',
    user     : 'root',
    password : '123456',
    database : 'QtTesting'
});
connection.connect();

connection.query('SELECT * FROM position ', function (error, results, fields) {
    if (error) throw error;
    console.log('testing', results[0].longitude);
});