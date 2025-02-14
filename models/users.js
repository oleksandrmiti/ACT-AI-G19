const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    resetToken: { type: String, required: false }, 
    resetTokenExpiration: { type: Date, required: false } 
});

const User = mongoose.model('User', UserSchema);
module.exports = User;

