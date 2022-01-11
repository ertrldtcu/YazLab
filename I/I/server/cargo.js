function addCargo(db, userID, cargo, res) {

    var sql = "INSERT INTO cargos (userID,customerName,address,lat,lng,status) VALUES ('" + userID + "','" + cargo.customerName + "','" + cargo.address + "'," + cargo.lat + "," + cargo.lng + ",0)";
    db.query(sql, (err, result) => {
        if (err) throw err;
        console.log(typeof result.insertId, result.insertId);
        res.send(JSON.stringify(result.insertId));
    });

}

function removeCargo(db, cargoID) {
    var sql = "DELETE FROM cargos WHERE id = '" + parseInt(cargoID) + "'";
    db.query(sql, () => {});
}

function updateCargoStatus(db, cargoID, newStatus) {

    console.log(typeof newStatus, newStatus);

    var sql = "UPDATE cargos SET status=" + newStatus + " WHERE id='" + cargoID + "'"
    db.query(sql, () => {});
}

module.exports = {
    addCargo,
    removeCargo,
    updateCargoStatus
}