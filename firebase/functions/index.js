const functions = require('firebase-functions');
const botCommands = require('./bot-commands');
const {Telegraf} = require('telegraf');



const bot = new Telegraf(functions.config().telegram.token, {
    telegram: {webhookReply: true},
});

// commands
botCommands.handleCommands(bot);

exports.bot = functions.https.onRequest(async (request, response) => {
    functions.logger.log('Incoming message', request.body)
    return await bot.handleUpdate(request.body, response).then((rv) => {
        // if it's not a request from the telegram, rv will be undefined, but we should respond with 200
        // eslint-disable-next-line promise/always-return
        return true;
    })
})