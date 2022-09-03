
async def SendMessage(context, message):
    return await context.channel.send('<@' + str(context.author.id) + '> ' + message)

async def SendMessageById(context, id, message):
    return await context.channel.send('<@' + str(id) + '> ' + message)