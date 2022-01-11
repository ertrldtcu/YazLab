function login(db, username, password, res) {
    var sql = "SELECT id FROM users WHERE username = '" + username + "' AND password = '" + password + "'";
    db.query(sql, (err, result) => {
        if (Object.keys(result).length > 0) {
            sql = "SELECT * FROM cargos WHERE userID = '" + parseInt(result[0].id) + "'";
            db.query(sql, (err, cargos) => {
                res.send(JSON.stringify({
                    userID: result[0].id,
                    cargos: JSON.stringify(cargos)
                }));
            })
        }
    });
}

module.exports = {
    login
}