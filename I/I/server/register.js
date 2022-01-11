function register(db, username, password, res) {

    var sql = "SELECT id FROM users WHERE username = '" + username + "'";
    db.query(sql, (err, result) => {

        if (err) {} else {

            if (Object.keys(result).length == 0) {

                sql = "INSERT INTO users (username,password) VALUES ('" + username + "','" + password + "')";
                db.query(sql, (err) => {});
            }
        }
    });
}

module.exports = {
    register
};