const firebase = require('firebase-admin');

const firebaseApp = firebase.initializeApp();
const usersRef = firebaseApp.database().ref('users');

const addEtfs = (chatId, etfs) => {
    usersRef.orderByKey().startAt(chatId).once('value', (snapshot) => {
        if (snapshot.numChildren() > 0) {
            const key = Object.keys(snapshot.val())[0];
            let currentEtfs = snapshot.val()[key].etfs || [];
            currentEtfs = currentEtfs.filter((etf) => etfs.findIndex((e) => e === etf) === -1);
            usersRef.child(key).update({
                etfs: etfs.concat(currentEtfs),
            })
        }
    });
}

const removeEtfs = (chatId, etfs) => {
    usersRef.orderByKey().startAt(chatId).once('value', (snapshot) => {
        if (snapshot.numChildren() > 0) {
            const key = Object.keys(snapshot.val())[0];
            const currentEtfs = snapshot.val()[key].etfs|| [];
            usersRef.child(key).update({
                etfs: currentEtfs.filter((etf) => etfs.findIndex((e) => e === etf) === -1),
            })
        }
    });
}

const moveEtf = (chatId, etf, position) => {
    usersRef.orderByKey().startAt(chatId).once('value', (snapshot) => {
        if (snapshot.numChildren() > 0) {
            const key = Object.keys(snapshot.val())[0];
            let currentEtfs = snapshot.val()[key].etfs|| [];
            const currentEtfIndex = currentEtfs.findIndex((e) => e === etf);
            currentEtfs = moveElementInArray(currentEtfs,currentEtfIndex, position);
            usersRef.child(key).update({
                etfs: currentEtfs,
            })
        }
    });
}

const moveElementInArray = (arr, old_index, new_index) => {
    if (new_index >= arr.length) {
        var k = new_index - arr.length + 1;
        while (k--) {
            arr.push(undefined);
        }
    }
    arr.splice(new_index, 0, arr.splice(old_index, 1)[0]);
    return arr;
};

const getEtfsFromMessage = (message) => {
    const etfsText = message.split(new RegExp("add|remove|move"))[1].trim();
    if (etfsText === "")
        throw "No etfs provided!";
    return etfsText.split(" ").map((etf) => etf.toUpperCase());
}

/**
 * Handling commands comming from telegram
 * @param bot
 */

exports.handleCommands = (bot) => {
    // command to start the configurations
    bot.command('/start', (ctx) => {
        const chatId = ctx.message.chat.id.toString();
        const token = Math.floor(1000 + Math.random() * 9000).toString();
        usersRef.orderByKey().startAt(chatId).once('value', (snapshot) => {
            let key = chatId + '-' + token;
            if (snapshot.numChildren() > 0) {
                key = Object.keys(snapshot.val())[0];
            } else {
                usersRef.child(key).set({
                    id: chatId,
                });
            }
            ctx.reply('Welcome! Use the following code to connect your display => ' + key);
        });
    });

    // add a certain etf
    bot.command('/add', (ctx) => {
        const chatId = ctx.message.chat.id.toString();
        const message = ctx.message.text.trim();
        try {
            const etfs = getEtfsFromMessage(message);
            addEtfs(chatId, etfs);
            ctx.reply(etfs.join(",") + " has been added!");

        } catch (e) {
            ctx.reply("Valid Syntax: /add btc goog amzn");
        }
    });

    // remove a certain etf
    bot.command('/remove', (ctx) => {
        const chatId = ctx.message.chat.id.toString();
        const message = ctx.message.text.trim();

        try {
            const etfs = getEtfsFromMessage(message);
            removeEtfs(chatId, etfs);
            ctx.reply(etfs.join(",") + " has been remove!");
        } catch (e) {
            ctx.reply("** Remove an existing ticker.")
            ctx.reply("** Valid Syntax: /remove btc goog amzn");
        }
    });

    // move command
    bot.command('/move', (ctx) => {
        const chatId = ctx.message.chat.id.toString();
        const message = ctx.message.text.trim();

        try {
            const result = getEtfsFromMessage(message);
            const ticker = result[0];
            const position = parseInt(result[1]) - 1; // array start from 0
            moveEtf(chatId, ticker, position);
            ctx.reply(ticker + " has been moved to position => " + result[1]);
        } catch (e) {
            ctx.reply("** Valid Syntax: /move btc 0");
        }
    })
};